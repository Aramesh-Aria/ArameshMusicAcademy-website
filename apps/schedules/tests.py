from datetime import date, time
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from apps.teachers.models import Instrument, Teacher

from .models import ClassSession, Weekday


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
        self.assertEqual(rows[0]['instruments'], [self.instrument])
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
