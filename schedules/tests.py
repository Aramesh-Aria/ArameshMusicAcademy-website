from datetime import time

import jdatetime
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from teachers.models import Instrument, Teacher

from .models import ClassSession, Course, Weekday


class ClassSessionModelTests(TestCase):
    def setUp(self):
        instrument = Instrument.objects.create(name='Piano')
        self.teacher = Teacher.objects.create(
            first_name='Sara',
            last_name='Karimi',
            date_of_birth=jdatetime.date(1363, 1, 1),
            birth_province='Tehran',
            birth_city='Tehran',
            education='Music MA',
            biography='Biography',
            profile_image='teachers/sara.jpg',
        )
        self.teacher.instruments.add(instrument)
        self.course = Course.objects.create(name='Piano')

    def test_end_time_must_be_after_start_time(self):
        session = ClassSession(
            course=self.course,
            teacher=self.teacher,
            weekday=Weekday.SATURDAY,
            start_time=time(12, 0),
            end_time=time(11, 0),
        )

        with self.assertRaises(ValidationError):
            session.full_clean()


class ScheduleViewTests(TestCase):
    def setUp(self):
        instrument = Instrument.objects.create(name='Guitar')
        self.teacher = Teacher.objects.create(
            first_name='Reza',
            last_name='Moradi',
            date_of_birth=jdatetime.date(1359, 2, 11),
            birth_province='Fars',
            birth_city='Shiraz',
            education='Music BA',
            biography='Biography',
            profile_image='teachers/reza.jpg',
        )
        self.teacher.instruments.add(instrument)
        self.course = Course.objects.create(name='Guitar')

    def test_schedule_displays_persian_weekdays_and_active_sessions(self):
        ClassSession.objects.create(
            course=self.course,
            teacher=self.teacher,
            weekday=Weekday.SATURDAY,
            start_time=time(9, 0),
            end_time=time(10, 0),
            is_active=True,
        )
        ClassSession.objects.create(
            course=self.course,
            teacher=self.teacher,
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

# Create your tests here.
