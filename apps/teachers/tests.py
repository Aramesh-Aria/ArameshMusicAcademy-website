from datetime import time

from django.test import TestCase
from django.urls import reverse

from apps.schedules.models import ClassSession, Weekday

from .models import Instrument, Teacher


class TeacherModelTests(TestCase):
    def test_full_name_joins_first_and_last_name(self):
        teacher = Teacher(
            first_name='Ali',
            last_name='Ahmadi',
            biography='Teacher biography',
            profile_image='teachers/ali.jpg',
        )

        self.assertEqual(teacher.full_name, 'Ali Ahmadi')


class TeacherViewTests(TestCase):
    def setUp(self):
        self.instrument = Instrument.objects.create(name='Piano')

    def make_teacher(self, first_name, last_name, is_active=True, display_order=0):
        teacher = Teacher.objects.create(
            first_name=first_name,
            last_name=last_name,
            biography='Teacher biography',
            profile_image='teachers/example.jpg',
            is_active=is_active,
            display_order=display_order,
        )
        teacher.instruments.add(self.instrument)
        return teacher

    def test_teacher_list_shows_only_active_teachers_in_display_order(self):
        second = self.make_teacher('Sara', 'Karimi', display_order=2)
        first = self.make_teacher('Reza', 'Moradi', display_order=1)
        self.make_teacher('Hidden', 'Teacher', is_active=False)

        response = self.client.get(reverse('teachers:teacher_list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['teachers']), [first, second])
        self.assertContains(response, first.full_name)
        self.assertNotContains(response, 'Hidden Teacher')

    def test_teacher_page_previews_with_the_teachers_portrait(self):
        teacher = self.make_teacher('Sara', 'Karimi')

        response = self.client.get(teacher.get_absolute_url())

        self.assertContains(response, f'<meta property="og:image" content="https://aramesh-academy.ir{teacher.profile_image.url}">', html=True)

    def test_inactive_teacher_detail_returns_404(self):
        inactive_teacher = self.make_teacher('Hidden', 'Teacher', is_active=False)

        response = self.client.get(inactive_teacher.get_absolute_url())

        self.assertEqual(response.status_code, 404)

    def test_teacher_detail_lists_active_sessions(self):
        teacher = self.make_teacher('Sara', 'Karimi')
        session = ClassSession.objects.create(
            teacher=teacher,
            weekday=Weekday.SATURDAY,
            start_time=time(9, 0),
            end_time=time(10, 0),
            is_active=True,
        )
        session.instruments.add(self.instrument)

        response = self.client.get(teacher.get_absolute_url())

        self.assertIn(session, list(response.context['teacher_sessions']))
        self.assertContains(response, 'برنامهٔ هفتگی')

    def test_teacher_list_prefetches_active_sessions_in_week_order(self):
        teacher = self.make_teacher('Sara', 'Karimi')
        monday = ClassSession.objects.create(
            teacher=teacher, weekday=Weekday.MONDAY, start_time=time(9, 0), end_time=time(10, 0),
        )
        saturday = ClassSession.objects.create(
            teacher=teacher, weekday=Weekday.SATURDAY, start_time=time(9, 0), end_time=time(10, 0),
        )
        ClassSession.objects.create(
            teacher=teacher, weekday=Weekday.SUNDAY, start_time=time(9, 0), end_time=time(10, 0), is_active=False,
        )
        for index in range(3):
            self.make_teacher(f'Extra{index}', 'Teacher')

        # The gallery menu, then teachers, instruments and sessions: four queries however many teachers there are.
        with self.assertNumQueries(4):
            response = self.client.get(reverse('teachers:teacher_list'))
            teachers = list(response.context['teachers'])
            sessions = teachers[0].active_sessions

        self.assertEqual(sessions, [saturday, monday])
        self.assertContains(response, 'شنبه، دوشنبه')


class InstrumentModelTests(TestCase):
    def test_the_main_grid_leaves_out_childrens_instruments(self):
        santur = Instrument.objects.create(name='سنتور', slug='santur')
        Instrument.objects.create(name='بلز', slug='glockenspiel', children_only=True)

        self.assertEqual(list(Instrument.objects.main()), [santur])

    def test_an_instrument_made_without_a_slug_gets_one(self):
        latin = Instrument.objects.create(name='Piano')
        persian = Instrument.objects.create(name='سنتور')

        self.assertEqual(latin.slug, 'piano')
        self.assertEqual(persian.slug, f'instrument-{persian.pk}')
        self.assertEqual(Instrument.objects.get(pk=persian.pk).slug, persian.slug)
