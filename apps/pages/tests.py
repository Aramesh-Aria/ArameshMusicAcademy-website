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

        self.assertIn(teacher, list(response.context['featured_teachers']))
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
        self.assertEqual([day['weekday'] for day in days], [w.value for w in WEEKDAY_ORDER])
        self.assertEqual(days[0]['label'], 'شنبه')

    def test_week_schedule_groups_active_sessions_by_day_in_start_order(self):
        sara = self.make_teacher('Sara')
        reza = self.make_teacher('Reza')
        late = self.make_session(sara, Weekday.MONDAY, 16, 18)
        early = self.make_session(reza, Weekday.MONDAY, 10, 12)
        self.make_session(sara, Weekday.MONDAY, 12, 14, is_active=False)
        self.make_session(self.make_teacher('Gone', is_active=False), Weekday.MONDAY, 9, 10)

        response = self.client.get(reverse('pages:home'))

        monday = response.context['week_schedule'][2]
        self.assertEqual(monday['sessions'], [early, late])
        self.assertEqual(response.context['week_schedule'][0]['sessions'], [])

    @patch('apps.schedules.week.timezone.localdate', return_value=datetime.date(2026, 10, 26))  # a Monday
    def test_week_schedule_marks_today_in_tehran(self, _localdate):
        response = self.client.get(reverse('pages:home'))

        today = [day['weekday'] for day in response.context['week_schedule'] if day['is_today']]
        self.assertEqual(today, ['mon'])

    def test_week_schedule_renders_on_the_home_page(self):
        self.make_session(self.make_teacher('Sara'), Weekday.SATURDAY, 16, 18)

        response = self.client.get(reverse('pages:home'))

        self.assertContains(response, 'Sara Teacher')
        self.assertContains(response, '16:00')

    def test_featured_teachers_holds_the_director_and_three_more(self):
        for name in ['A', 'B', 'C', 'D', 'E']:
            self.make_teacher(name)

        response = self.client.get(reverse('pages:home'))

        self.assertEqual(len(response.context['featured_teachers']), 4)


class PageViewTests(TestCase):
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
