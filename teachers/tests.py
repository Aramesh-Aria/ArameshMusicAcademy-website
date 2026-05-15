import jdatetime
from django.test import TestCase
from django.urls import reverse

from .models import Instrument, Teacher


class TeacherModelTests(TestCase):
    def test_full_name_joins_first_and_last_name(self):
        teacher = Teacher(
            first_name='Ali',
            last_name='Ahmadi',
            date_of_birth=jdatetime.date(1363, 10, 11),
            birth_province='Tehran',
            birth_city='Tehran',
            education='Music BA',
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
            date_of_birth=jdatetime.date(1363, 10, 11),
            birth_province='Tehran',
            birth_city='Tehran',
            education='Music BA',
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

    def test_inactive_teacher_detail_returns_404(self):
        inactive_teacher = self.make_teacher('Hidden', 'Teacher', is_active=False)

        response = self.client.get(inactive_teacher.get_absolute_url())

        self.assertEqual(response.status_code, 404)

# Create your tests here.
