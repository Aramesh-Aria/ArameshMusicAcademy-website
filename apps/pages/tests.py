import datetime
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from apps.schedules.models import ClassSession, Weekday, WEEKDAY_ORDER
from apps.teachers.models import Instrument, Teacher
from apps.testimonials.models import Testimonial

from .models import SitePageContent


class HomeContextTests(TestCase):
    def test_home_context_includes_preview_sections(self):
        teacher = Teacher.objects.create(
            first_name='Sara',
            last_name='Karimi',
            biography='Bio',
            profile_image='teachers/sara.jpg',
            is_active=True,
        )
        Testimonial.objects.create(author_name='مادر آرمین', quote='عالی بود.', is_active=True)

        response = self.client.get(reverse('pages:home'))

        self.assertEqual(response.context['director'], teacher)
        self.assertEqual(len(response.context['testimonials']), 1)
        self.assertIn('gallery_preview_images', response.context)
        self.assertTrue(response.context['meta_description'])


class HomeWeekScheduleTests(TestCase):
    def make_teacher(self, first_name, is_active=True):
        return Teacher.objects.create(
            first_name=first_name,
            last_name='Teacher',
            biography='Bio',
            profile_image='teachers/example.jpg',
            is_active=is_active,
        )

    def make_session(self, teacher, weekday, start, end, is_active=True):
        session = ClassSession.objects.create(
            teacher=teacher,
            weekday=weekday,
            start_time=datetime.time(start),
            end_time=datetime.time(end),
            is_active=is_active,
        )
        session.instruments.set([self.piano])
        return session

    def setUp(self):
        self.piano = Instrument.objects.create(name='Piano')

    def test_week_schedule_lists_all_seven_days_from_saturday(self):
        response = self.client.get(reverse('pages:home'))

        days = response.context['week_schedule']
        self.assertEqual([day.weekday for day in days], [w.value for w in WEEKDAY_ORDER])
        self.assertEqual(days[0].label, 'شنبه')

    def test_week_schedule_groups_active_sessions_by_day_in_start_order(self):
        sara = self.make_teacher('Sara')
        reza = self.make_teacher('Reza')
        late = self.make_session(sara, Weekday.MONDAY, 16, 18)
        early = self.make_session(reza, Weekday.MONDAY, 10, 12)
        self.make_session(sara, Weekday.MONDAY, 12, 14, is_active=False)
        self.make_session(self.make_teacher('Gone', is_active=False), Weekday.MONDAY, 9, 10)

        response = self.client.get(reverse('pages:home'))

        monday = response.context['week_schedule'][2]
        self.assertEqual(monday.sessions, [early, late])
        self.assertEqual(response.context['week_schedule'][0].sessions, [])

    @patch('apps.schedules.week.timezone.localdate', return_value=datetime.date(2026, 10, 26))  # a Monday
    def test_week_schedule_marks_today_in_tehran(self, _localdate):
        response = self.client.get(reverse('pages:home'))

        today = [day.weekday for day in response.context['week_schedule'] if day.is_today]
        self.assertEqual(today, [Weekday.MONDAY])

    def test_week_schedule_renders_on_the_home_page(self):
        self.make_session(self.make_teacher('Sara'), Weekday.SATURDAY, 16, 18)

        response = self.client.get(reverse('pages:home'))

        self.assertContains(response, 'Sara Teacher')
        self.assertContains(response, '16:00')

    def test_template_comments_do_not_leak_into_the_page(self):
        response = self.client.get(reverse('pages:home'))

        self.assertNotContains(response, '{#')
        self.assertNotContains(response, '#}')

    def test_every_day_is_listed_under_its_own_heading_without_javascript(self):
        response = self.client.get(reverse('pages:home'))

        self.assertContains(response, 'class="day-heading"', count=7)
        self.assertNotContains(response, 'role="tabpanel"')

    def test_an_empty_day_on_the_home_page_links_to_the_full_week(self):
        response = self.client.get(reverse('pages:home'))

        self.assertContains(response, 'برنامهٔ کامل هفته')
        self.assertContains(response, 'جمعه‌ها آموزشگاه تعطیل است.')

    def test_home_shows_the_director_in_the_hero_and_three_more_teachers(self):
        for name in ['A', 'B', 'C', 'D', 'E']:
            self.make_teacher(name)

        response = self.client.get(reverse('pages:home'))

        self.assertIsNotNone(response.context['director'])
        self.assertEqual(len(response.context['home_teachers']), 3)
        self.assertNotIn(response.context['director'], response.context['home_teachers'])


    def test_the_director_intro_shows_beside_the_portrait_not_the_biography(self):
        director = self.make_teacher('A')
        director.home_intro = 'بنیان‌گذار آموزشگاه'
        director.biography = 'رزومهٔ کامل استاد'
        director.save()

        response = self.client.get(reverse('pages:home'))

        self.assertContains(response, '<p class="home-plate-intro">بنیان‌گذار آموزشگاه</p>', html=True)
        self.assertNotContains(response, 'رزومهٔ کامل استاد')

    def test_a_director_without_an_intro_shows_no_empty_paragraph(self):
        self.make_teacher('A')

        response = self.client.get(reverse('pages:home'))

        self.assertNotContains(response, 'home-plate-intro')


    def test_home_shows_at_most_three_testimonials_in_display_order(self):
        for order in range(5):
            Testimonial.objects.create(author_name=f'والد {order}', quote='خوب بود.', display_order=order, is_active=True)

        response = self.client.get(reverse('pages:home'))

        self.assertEqual([t.author_name for t in response.context['testimonials']], ['والد 0', 'والد 1', 'والد 2'])


class PageViewTests(TestCase):
    def test_home_without_admin_content_shows_visitor_copy_not_a_placeholder(self):
        response = self.client.get(reverse('pages:home'))

        self.assertContains(response, 'برای مشاوره و هماهنگی کلاس با ما تماس بگیرید.')
        self.assertNotContains(response, 'Django')

    def test_about_without_admin_content_shows_visitor_copy_not_a_placeholder(self):
        response = self.client.get(reverse('pages:about'))

        self.assertContains(response, 'آموزشگاه موسیقی آرامش جایی برای آموختن')
        self.assertNotContains(response, 'انتخاب قالب')

    def test_home_page_loads(self):
        response = self.client.get(reverse('pages:home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'آموزشگاه موسیقی آرامش')

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

# Create your tests here.


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

