import datetime
from unittest.mock import patch

from django.templatetags.static import static
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from apps.gallery.models import GalleryImage, GalleryPage
from apps.programmes.models import Programme
from apps.schedules.models import ClassSession, Weekday, WEEKDAY_ORDER
from apps.schedules.week import today_status, week_schedule
from apps.teachers.models import Instrument, Teacher
from apps.testimonials.models import Testimonial

from .models import FAQ, SitePageContent


def make_teacher(first_name, is_active=True):
    return Teacher.objects.create(
        first_name=first_name, last_name='Teacher', biography='Bio',
        profile_image='teachers/example.jpg', is_active=is_active,
    )


def make_session(teacher, weekday, start, end, instruments=(), is_active=True):
    session = ClassSession.objects.create(
        teacher=teacher, weekday=weekday, is_active=is_active,
        start_time=datetime.time(*start) if isinstance(start, tuple) else datetime.time(start),
        end_time=datetime.time(*end) if isinstance(end, tuple) else datetime.time(end),
    )
    session.instruments.set(instruments)
    return session


class WeekScheduleTests(TestCase):
    def setUp(self):
        self.piano = Instrument.objects.create(name='Piano', slug='piano')

    def test_week_schedule_lists_all_seven_days_from_saturday(self):
        days = week_schedule()

        self.assertEqual([day.weekday for day in days], [w.value for w in WEEKDAY_ORDER])
        self.assertEqual(days[0].label, 'شنبه')

    def test_week_schedule_groups_active_sessions_by_day_in_start_order(self):
        sara, reza = make_teacher('Sara'), make_teacher('Reza')
        late = make_session(sara, Weekday.MONDAY, 16, 18, [self.piano])
        early = make_session(reza, Weekday.MONDAY, 10, 12, [self.piano])
        make_session(sara, Weekday.MONDAY, 12, 14, [self.piano], is_active=False)
        make_session(make_teacher('Gone', is_active=False), Weekday.MONDAY, 9, 10, [self.piano])

        days = week_schedule()

        self.assertEqual(days[2].sessions, [early, late])
        self.assertEqual(days[0].sessions, [])

    @patch('apps.schedules.week.timezone.localdate', return_value=datetime.date(2026, 10, 26))  # a Monday
    def test_week_schedule_marks_today_in_tehran(self, _localdate):
        today = [day.weekday for day in week_schedule() if day.is_today]

        self.assertEqual(today, [Weekday.MONDAY])


@patch('apps.schedules.week.timezone.localdate', return_value=datetime.date(2026, 10, 26))  # a Monday
class TodayStatusTests(TestCase):
    def setUp(self):
        self.santur = Instrument.objects.create(name='سنتور', slug='santur', display_order=1)
        self.piano = Instrument.objects.create(name='پیانو', slug='piano', display_order=2)
        self.bells = Instrument.objects.create(name='بلز', slug='bells', children_only=True)
        self.children = Programme.objects.create(
            name='موسیقی کودک', slug='children', short_description='.', long_description='.',
        )
        sara = make_teacher('Sara')
        sara.programmes.add(self.children)
        make_session(sara, Weekday.MONDAY, 10, 14, [self.piano, self.bells])
        make_session(make_teacher('Reza'), Weekday.MONDAY, 15, (19, 30), [self.santur])
        make_session(sara, Weekday.WEDNESDAY, 11, 13, [self.piano])

    def at(self, hour):
        return timezone.make_aware(datetime.datetime(2026, 10, 26, hour))

    def test_while_classes_run_it_names_what_is_taught_until_when(self, _localdate):
        today = today_status(week_schedule(), now=self.at(12))

        self.assertEqual(today.state, 'open')
        self.assertEqual(today.day_label, 'دوشنبه')
        self.assertEqual(today.taught, ['سنتور', 'پیانو', 'موسیقی کودک'])  # no children-only instrument
        self.assertEqual(today.until, datetime.time(19, 30))

    def test_before_the_first_class_it_says_from_when(self, _localdate):
        today = today_status(week_schedule(), now=self.at(8))

        self.assertEqual(today.state, 'before')
        self.assertEqual((today.since, today.until), (datetime.time(10), datetime.time(19, 30)))

    def test_before_the_first_class_the_home_page_says_from_when(self, _localdate):
        with patch('apps.schedules.week.timezone.localtime', return_value=self.at(8)):
            response = self.client.get(reverse('pages:home'))

        self.assertContains(response, '<b>امروز، دوشنبه:</b> سنتور، پیانو، موسیقی کودک، از ساعت 10 تا 19:30', html=False)

    def test_after_the_last_class_it_says_when_classes_resume(self, _localdate):
        today = today_status(week_schedule(), now=self.at(20))

        self.assertEqual(today.state, 'over')
        self.assertEqual((today.next_label, today.next_from), ('چهارشنبه', datetime.time(11)))

    def test_the_home_page_renders_the_line(self, _localdate):
        with patch('apps.schedules.week.timezone.localtime', return_value=self.at(12)):
            response = self.client.get(reverse('pages:home'))

        self.assertContains(response, '<b>امروز، دوشنبه:</b> سنتور، پیانو، موسیقی کودک، تا ساعت 19:30', html=False)


class HomePageTests(TestCase):
    def test_the_hero_crossfades_the_home_hero_photos_with_their_titles(self):
        hero = GalleryPage.objects.create(title='تصاویر صفحه اصلی', slug='home-hero')
        GalleryImage.objects.create(gallery_page=hero, image='gallery/a.jpg', title='کلاس سنتور', display_order=1)
        GalleryImage.objects.create(gallery_page=hero, image='gallery/b.jpg', title='کلاس پیانو', display_order=2)

        response = self.client.get(reverse('pages:home'))

        self.assertEqual([s.title for s in response.context['hero_slides']], ['کلاس سنتور', 'کلاس پیانو'])
        self.assertContains(response, 'class="hero__bar"', count=2)
        self.assertContains(response, 'fetchpriority="high"', count=1)

    def test_a_hero_photo_keeps_its_focal_point_in_the_frame(self):
        hero = GalleryPage.objects.create(title='تصاویر صفحه اصلی', slug='home-hero')
        GalleryImage.objects.create(
            gallery_page=hero, image='gallery/a.jpg', title='کلاس سنتور', display_order=1,
            focal_point=GalleryImage.FocalPoint.BOTTOM_LEFT,
        )
        GalleryImage.objects.create(gallery_page=hero, image='gallery/b.jpg', title='کلاس پیانو', display_order=2)

        response = self.client.get(reverse('pages:home'))

        self.assertContains(response, 'style="object-position: 25% 75%"', count=1)

    def test_the_link_preview_is_the_logo_image_not_a_hero_photo(self):
        hero = GalleryPage.objects.create(title='تصاویر صفحه اصلی', slug='home-hero')
        GalleryImage.objects.create(gallery_page=hero, image='gallery/a.jpg', title='کلاس سنتور', display_order=1)

        response = self.client.get(reverse('pages:home'))

        self.assertContains(response, f'<meta property="og:image" content="https://aramesh-academy.ir{static("assets/img/og-image.jpg")}">', html=True)
        self.assertContains(response, '<meta property="og:image:width" content="1200">', html=True)
        self.assertContains(response, '<meta property="og:image:height" content="630">', html=True)
        self.assertContains(response, '<meta property="og:image:type" content="image/jpeg">', html=True)
        self.assertNotContains(response, 'content="https://aramesh-academy.ir/public/media/')

    def test_without_hero_photos_the_frame_holds_the_santur_shape(self):
        response = self.client.get(reverse('pages:home'))

        self.assertContains(response, 'hero__frame frame frame--shape')
        self.assertNotContains(response, 'hero__bar')

    def test_programmes_instruments_and_teachers_are_listed(self):
        Programme.objects.create(name='گروه نوازی', slug='ensemble', short_description='پنجشنبه‌ها', long_description='.')
        Instrument.objects.create(name='سنتور', slug='santur')
        Instrument.objects.create(name='بلز', slug='bells', children_only=True)
        teacher = make_teacher('Sara')
        teacher.lineage = 'شاگرد استاد'
        teacher.save()

        response = self.client.get(reverse('pages:home'))

        self.assertContains(response, 'پنجشنبه‌ها')
        self.assertContains(response, 'href="/instruments/santur/"')
        self.assertNotContains(response, 'بلز')
        self.assertContains(response, 'شاگرد استاد')

    def test_teaching_and_first_lesson_render_as_points_and_ordered_steps(self):
        SitePageContent.objects.create(page_key=SitePageContent.TEACHING, title='شیوهٔ آموزش', body='یک استاد\nمتن')
        SitePageContent.objects.create(page_key=SitePageContent.FIRST_LESSON, title='سه قدم', body='تماس بگیرید\nمتن')

        response = self.client.get(reverse('pages:home'))

        self.assertContains(response, '<h3>یک استاد</h3>', html=True)
        self.assertContains(response, '<ol class="steps">')

    def test_empty_sections_are_hidden(self):
        response = self.client.get(reverse('pages:home'))

        for marker in ('marquee', 'accordion', 'programme-row', 'tile-grid', 'portrait-row', 'class="mosaic"', 'teaching'):
            self.assertNotContains(response, marker)
        self.assertContains(response, 'class="band"')

    def test_up_to_eight_testimonials_run_in_the_marquee_once_for_readers(self):
        for order in range(10):
            Testimonial.objects.create(author_name=f'والد {order}', quote='خوب بود.', display_order=order)

        response = self.client.get(reverse('pages:home'))

        self.assertEqual(len(response.context['testimonials']), 8)
        self.assertContains(response, 'class="marquee__list" role="list" aria-hidden="true"', count=1)

    def test_a_single_testimonial_stands_still_and_is_listed_once(self):
        Testimonial.objects.create(author_name='فاطمه حسینی', quote='دخترم اینجا پیانو می‌زند.')

        response = self.client.get(reverse('pages:home'))

        self.assertContains(response, 'class="marquee marquee--still"')
        self.assertContains(response, 'دخترم اینجا پیانو می‌زند.', count=1)

    def test_only_active_faqs_marked_for_home_show(self):
        FAQ.objects.create(question='بهترین سن؟', answer='.')
        FAQ.objects.create(question='فقط صفحهٔ دوره', answer='.', show_on_home=False)
        FAQ.objects.create(question='غیرفعال', answer='.', is_active=False)

        response = self.client.get(reverse('pages:home'))

        self.assertContains(response, 'بهترین سن؟')
        self.assertNotContains(response, 'فقط صفحهٔ دوره')
        self.assertNotContains(response, 'غیرفعال')

    def test_template_comments_do_not_leak_into_the_page(self):
        response = self.client.get(reverse('pages:home'))

        self.assertNotContains(response, '{#')
        self.assertNotContains(response, '#}')


class PageViewTests(TestCase):
    def test_home_without_admin_content_shows_visitor_copy_not_a_placeholder(self):
        response = self.client.get(reverse('pages:home'))

        self.assertContains(response, 'موسیقی، در فضایی آرام')
        self.assertNotContains(response, 'Django')

    def test_about_without_admin_content_shows_visitor_copy_not_a_placeholder(self):
        response = self.client.get(reverse('pages:about'))

        self.assertContains(response, 'آموزشگاه موسیقی آرامش جایی برای آموختن')
        self.assertNotContains(response, 'انتخاب قالب')

    def test_home_page_loads(self):
        response = self.client.get(reverse('pages:home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'آموزشگاه موسیقی آرامش')

    @override_settings(ABOUT_GALLERY_SLUG='academy-space')
    def test_about_link_preview_is_the_logo_image_not_a_gallery_photo(self):
        space = GalleryPage.objects.create(title='فضای آموزشگاه', slug='academy-space')
        GalleryImage.objects.create(gallery_page=space, image='gallery/room.jpg', title='کلاس')

        response = self.client.get(reverse('pages:about'))

        self.assertContains(response, f'property="og:image" content="https://aramesh-academy.ir{static("assets/img/og-image.jpg")}"')
        self.assertNotContains(response, 'content="https://aramesh-academy.ir/public/media/')

    def test_about_page_loads(self):
        response = self.client.get(reverse('pages:about'))

        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_admin_managed_content_when_available(self):
        SitePageContent.objects.create(
            page_key=SitePageContent.HOME,
            title='خانه جدید',
            body='متن صفحه خانه از پنل مدیریت.',
            is_active=True,
        )

        response = self.client.get(reverse('pages:home'))

        self.assertContains(response, 'خانه جدید')
        self.assertContains(response, 'متن صفحه خانه از پنل مدیریت.')



class SitePageContentPointsTests(TestCase):
    def test_points_split_the_body_into_titles_and_texts(self):
        content = SitePageContent(
            page_key=SitePageContent.TEACHING,
            title='شیوهٔ آموزش',
            body='یک استاد، یک هنرجو\r\nهمهٔ کلاس‌ها خصوصی است.\r\nخط دوم.\r\n\r\n\r\nاز کلاس تا صحنه\nکنسرت‌های داخلی\n\nفقط عنوان',
        )

        self.assertEqual(content.points(), [
            ('یک استاد، یک هنرجو', 'همهٔ کلاس‌ها خصوصی است. خط دوم.'),
            ('از کلاس تا صحنه', 'کنسرت‌های داخلی'),
            ('فقط عنوان', ''),
        ])

