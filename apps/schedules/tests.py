from datetime import date, time
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from apps.programmes.models import Programme
from apps.teachers.models import Instrument, Teacher

from .admin import ClassSessionForm
from .models import ClassSession, Weekday
from .week import active_sessions


class ClassSessionModelTests(TestCase):
    def setUp(self):
        self.instrument = Instrument.objects.create(name='Piano')
        self.teacher = Teacher.objects.create(
            first_name='Sara',
            last_name='Karimi',
            biography='Biography',
            profile_image='teachers/sara.jpg',
        )
        self.teacher.instruments.add(self.instrument)

    def test_end_time_must_be_after_start_time(self):
        session = ClassSession(
            teacher=self.teacher,
            weekday=Weekday.SATURDAY,
            start_time=time(12, 0),
            end_time=time(11, 0),
        )

        with self.assertRaises(ValidationError) as context:
            session.full_clean()

        self.assertIn('ساعت پایان باید بعد از ساعت شروع باشد.', context.exception.message_dict['end_time'])

    def test_active_sessions_for_same_teacher_cannot_overlap(self):
        ClassSession.objects.create(
            teacher=self.teacher,
            weekday=Weekday.SATURDAY,
            start_time=time(9, 0),
            end_time=time(10, 0),
            is_active=True,
        )
        overlapping_session = ClassSession(
            teacher=self.teacher,
            weekday=Weekday.SATURDAY,
            start_time=time(9, 30),
            end_time=time(10, 30),
            is_active=True,
        )

        with self.assertRaises(ValidationError):
            overlapping_session.full_clean(exclude=['instruments'])

    def test_inactive_sessions_can_overlap(self):
        ClassSession.objects.create(
            teacher=self.teacher,
            weekday=Weekday.SATURDAY,
            start_time=time(9, 0),
            end_time=time(10, 0),
            is_active=True,
        )
        overlapping_session = ClassSession(
            teacher=self.teacher,
            weekday=Weekday.SATURDAY,
            start_time=time(9, 30),
            end_time=time(10, 30),
            is_active=False,
        )

        overlapping_session.full_clean(exclude=['instruments'])


class ScheduleViewTests(TestCase):
    def setUp(self):
        self.instrument = Instrument.objects.create(name='Guitar')
        self.teacher = Teacher.objects.create(
            first_name='Reza',
            last_name='Moradi',
            biography='Biography',
            profile_image='teachers/reza.jpg',
        )
        self.teacher.instruments.add(self.instrument)

    def _make_session(self, **kwargs):
        session = ClassSession.objects.create(teacher=self.teacher, **kwargs)
        session.instruments.add(self.instrument)
        return session

    def test_schedule_table_names_a_sessions_instruments_when_it_teaches_part_of_the_list(self):
        self._make_session(weekday=Weekday.SATURDAY, start_time=time(9, 0), end_time=time(10, 0), is_active=True)
        violin = Instrument.objects.create(name='Violin')
        self._make_session(weekday=Weekday.SUNDAY, start_time=time(9, 0), end_time=time(10, 0), is_active=True).instruments.add(violin)

        response = self.client.get(reverse('schedules:schedule'))

        # Saturday teaches guitar only, part of the row's guitar and violin; Sunday teaches both.
        self.assertContains(response, '<small class="week-instruments">Guitar</small>', html=True)
        self.assertContains(response, 'class="week-instruments"', count=1)

    def test_schedule_displays_persian_weekdays_and_active_sessions(self):
        self._make_session(
            weekday=Weekday.SATURDAY,
            start_time=time(9, 0),
            end_time=time(10, 0),
            is_active=True,
        )
        self._make_session(
            weekday=Weekday.SUNDAY,
            start_time=time(11, 0),
            end_time=time(12, 0),
            is_active=False,
        )

        response = self.client.get(reverse('schedules:schedule'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'شنبه')
        self.assertContains(response, 'Guitar')
        self.assertNotContains(response, '11:00')

    def test_schedule_orders_sessions_by_persian_weekday_order(self):
        self._make_session(
            weekday=Weekday.FRIDAY,
            start_time=time(9, 0),
            end_time=time(10, 0),
            is_active=True,
        )
        self._make_session(
            weekday=Weekday.SATURDAY,
            start_time=time(11, 0),
            end_time=time(12, 0),
            is_active=True,
        )

        response = self.client.get(reverse('schedules:schedule'))
        row = response.context['schedule_rows'][0]

        self.assertEqual(row['cells'][0].weekday, Weekday.SATURDAY)
        self.assertEqual(row['cells'][-1].weekday, Weekday.FRIDAY)
        self.assertEqual(row['cells'][0].sessions[0].start_time, time(11, 0))
        self.assertEqual(row['cells'][-1].sessions[0].start_time, time(9, 0))

    def test_schedule_context_contains_teacher_rows_with_instruments(self):
        self._make_session(
            weekday=Weekday.SATURDAY,
            start_time=time(9, 0),
            end_time=time(10, 0),
            is_active=True,
        )

        response = self.client.get(reverse('schedules:schedule'))
        rows = response.context['schedule_rows']

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['teacher'], self.teacher)
        self.assertEqual(rows[0]['offerings'].instruments, [self.instrument])
        self.assertEqual(rows[0]['cells'][0].weekday, Weekday.SATURDAY)
        self.assertEqual(len(rows[0]['cells'][0].sessions), 1)

    @patch('apps.schedules.week.timezone.localdate', return_value=date(2026, 10, 26))  # a Monday
    def test_schedule_marks_today_and_gives_the_week_by_day(self, _localdate):
        self._make_session(
            weekday=Weekday.MONDAY,
            start_time=time(9, 0),
            end_time=time(10, 0),
            is_active=True,
        )

        response = self.client.get(reverse('schedules:schedule'))
        week = response.context['week_schedule']

        self.assertEqual([day.weekday for day in week if day.is_today], [Weekday.MONDAY])
        row = response.context['schedule_rows'][0]
        self.assertEqual([cell.weekday for cell in row['cells'] if cell.is_today], [Weekday.MONDAY])
        self.assertEqual(len(week[2].sessions), 1)
        self.assertContains(response, '<td class="is-today">', html=False)


class ScheduleDisplayRuleTests(TestCase):
    """ClassSession.offerings(): what the schedule shows for each session (ADR-0002)."""

    def setUp(self):
        self.piano = Instrument.objects.create(name='پیانو', slug='piano', display_order=1)
        self.guitar = Instrument.objects.create(name='گیتار پاپ', slug='pop-guitar', display_order=2)
        self.bells = Instrument.objects.create(name='بلز', slug='glockenspiel', display_order=3, children_only=True)
        self.theory = Programme.objects.create(
            name='تئوری و سلفژ', slug='theory', kind=Programme.Kind.WITH_TEACHER,
            short_description='-', long_description='-',
        )
        self.ensemble = Programme.objects.create(
            name='گروه نوازی', slug='ensemble', kind=Programme.Kind.FIXED_TIME,
            short_description='-', long_description='-',
        )
        self.teacher = Teacher.objects.create(
            first_name='علی', last_name='شمس', biography='.', profile_image='teachers/ali.jpg',
        )
        self.teacher.programmes.add(self.theory)

    def _session(self, weekday, *instruments, programme=None):
        session = ClassSession.objects.create(
            teacher=self.teacher, weekday=weekday, start_time=time(14, 0), end_time=time(21, 0), programme=programme,
        )
        session.instruments.add(*instruments)
        return session

    def test_a_session_shows_its_instruments_then_the_teachers_programmes(self):
        session = self._session(Weekday.WEDNESDAY, self.guitar, self.piano)

        self.assertEqual(str(session.offerings()), 'پیانو، گیتار پاپ · تئوری و سلفژ')

    def test_a_reserved_session_shows_only_its_programme(self):
        session = self._session(Weekday.THURSDAY, programme=self.ensemble)

        offerings = session.offerings()
        self.assertEqual(offerings.instruments, [])
        self.assertEqual(offerings.programmes, [self.ensemble])
        self.assertEqual(str(offerings), 'گروه نوازی')

    def test_children_only_instruments_never_show_on_the_schedule(self):
        session = self._session(Weekday.SATURDAY, self.bells, self.piano)

        self.assertEqual(str(session.offerings()), 'پیانو · تئوری و سلفژ')

    def test_a_session_of_only_childrens_instruments_shows_the_teachers_programme(self):
        children = Programme.objects.create(
            name='موسیقی کودک', slug='children', kind=Programme.Kind.WITH_TEACHER,
            instruments_shown=Programme.InstrumentsShown.CHILDREN_ONLY,
            short_description='-', long_description='-',
        )
        self.teacher.programmes.set([children])
        session = self._session(Weekday.SATURDAY, self.bells)

        self.assertEqual(str(session.offerings()), 'موسیقی کودک')

    def test_an_inactive_programme_is_left_out(self):
        self.theory.is_active = False
        self.theory.save()
        session = self._session(Weekday.WEDNESDAY, self.piano)

        self.assertEqual(str(session.offerings()), 'پیانو')

    def test_offerings_read_from_the_prefetch_without_more_queries(self):
        self._session(Weekday.WEDNESDAY, self.piano)
        self._session(Weekday.THURSDAY, programme=self.ensemble)
        sessions = list(active_sessions())

        with self.assertNumQueries(0):
            [str(session.offerings()) for session in sessions]

    def test_the_schedule_page_shows_the_reserved_session_and_the_teachers_full_list(self):
        self._session(Weekday.WEDNESDAY, self.piano, self.guitar)
        self._session(Weekday.THURSDAY, programme=self.ensemble)

        response = self.client.get(reverse('schedules:schedule'))

        row = response.context['schedule_rows'][0]
        self.assertEqual(str(row['offerings']), 'پیانو، گیتار پاپ · تئوری و سلفژ، گروه نوازی')
        # Each session offers less than the row's full list, so each cell names its own.
        self.assertContains(response, '<small class="week-instruments">گروه نوازی</small>', html=True)
        self.assertContains(
            response, '<small class="week-instruments">پیانو، گیتار پاپ · تئوری و سلفژ</small>', html=True,
        )


class ClassSessionAdminFormTests(TestCase):
    def setUp(self):
        self.piano = Instrument.objects.create(name='پیانو', slug='piano')
        self.ensemble = Programme.objects.create(
            name='گروه نوازی', slug='ensemble', kind=Programme.Kind.FIXED_TIME,
            short_description='-', long_description='-',
        )
        self.theory = Programme.objects.create(
            name='تئوری و سلفژ', slug='theory', kind=Programme.Kind.WITH_TEACHER,
            short_description='-', long_description='-',
        )
        self.teacher = Teacher.objects.create(
            first_name='مسعود', last_name='آرامش', biography='.', profile_image='teachers/m.jpg',
        )

    def _form(self, **data):
        return ClassSessionForm(data={
            'teacher': self.teacher.pk, 'weekday': Weekday.THURSDAY,
            'start_time': '10:00', 'end_time': '19:00', 'is_active': True, **data,
        })

    def test_a_session_needs_instruments_or_a_reserved_programme(self):
        form = self._form()

        self.assertFalse(form.is_valid())
        self.assertIn('instruments', form.errors)

    def test_a_reserved_session_with_no_instruments_is_valid(self):
        self.assertTrue(self._form(programme=self.ensemble.pk).is_valid())

    def test_a_session_cannot_have_both_instruments_and_a_reserved_programme(self):
        form = self._form(programme=self.ensemble.pk, instruments=[self.piano.pk])

        self.assertFalse(form.is_valid())
        self.assertTrue(form.non_field_errors())

    def test_only_fixed_time_programmes_can_be_reserved(self):
        form = self._form(programme=self.theory.pk)

        self.assertFalse(form.is_valid())
        self.assertIn('programme', form.errors)
