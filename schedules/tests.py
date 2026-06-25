from datetime import time

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from teachers.models import Instrument, Teacher

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

        self.assertEqual(row['cells'][0]['weekday'], Weekday.SATURDAY)
        self.assertEqual(row['cells'][-1]['weekday'], Weekday.FRIDAY)
        self.assertEqual(row['cells'][0]['sessions'][0].start_time, time(11, 0))
        self.assertEqual(row['cells'][-1]['sessions'][0].start_time, time(9, 0))

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
        self.assertEqual(rows[0]['cells'][0]['weekday'], Weekday.SATURDAY)
        self.assertEqual(len(rows[0]['cells'][0]['sessions']), 1)
