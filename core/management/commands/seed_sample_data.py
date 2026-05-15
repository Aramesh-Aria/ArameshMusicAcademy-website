from datetime import time
from io import BytesIO

import jdatetime
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw

from schedules.models import ClassSession, Course, Weekday
from teachers.models import Instrument, Teacher


class Command(BaseCommand):
    help = 'Create sample music academy data for local development.'

    def handle(self, *args, **options):
        instruments = self.create_instruments()
        teachers = self.create_teachers(instruments)
        courses = self.create_courses()
        self.create_class_sessions(courses, teachers)

        self.stdout.write(self.style.SUCCESS('Sample academy data is ready.'))

    def create_instruments(self):
        instrument_names = ['پیانو', 'گیتار', 'ویولن', 'آواز']
        return {
            name: Instrument.objects.get_or_create(name=name)[0]
            for name in instrument_names
        }

    def create_teachers(self, instruments):
        teacher_data = [
            {
                'first_name': 'سارا',
                'last_name': 'کریمی',
                'instruments': ['پیانو'],
                'date_of_birth': jdatetime.date(1365, 2, 12),
                'birth_province': 'تهران',
                'birth_city': 'تهران',
                'education': 'کارشناسی ارشد نوازندگی پیانو',
                'biography': 'مدرس پیانو با تمرکز بر تکنیک، سلفژ و اجرای کلاسیک.',
                'display_order': 1,
                'image_color': '#6A8D73',
            },
            {
                'first_name': 'رضا',
                'last_name': 'مرادی',
                'instruments': ['گیتار'],
                'date_of_birth': jdatetime.date(1360, 7, 5),
                'birth_province': 'فارس',
                'birth_city': 'شیراز',
                'education': 'کارشناسی موسیقی',
                'biography': 'مدرس گیتار کلاسیک و پاپ با تجربه اجرای صحنه‌ای.',
                'display_order': 2,
                'image_color': '#8E6C88',
            },
            {
                'first_name': 'نگار',
                'last_name': 'احمدی',
                'instruments': ['ویولن', 'آواز'],
                'date_of_birth': jdatetime.date(1368, 11, 20),
                'birth_province': 'اصفهان',
                'birth_city': 'اصفهان',
                'education': 'کارشناسی ارشد آهنگسازی',
                'biography': 'مدرس ویولن و آواز با رویکرد مرحله‌ای برای هنرجویان مبتدی.',
                'display_order': 3,
                'image_color': '#C08457',
            },
        ]

        teachers = {}
        for data in teacher_data:
            instrument_names = data.pop('instruments')
            image_color = data.pop('image_color')
            teacher, _ = Teacher.objects.update_or_create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                defaults=data,
            )
            teacher.instruments.set(instruments[name] for name in instrument_names)
            self.ensure_teacher_image(teacher, image_color)
            teachers[teacher.full_name] = teacher
        return teachers

    def create_courses(self):
        course_names = ['کلاس پیانو', 'کلاس گیتار', 'کلاس ویولن', 'کلاس آواز']
        return {
            name: Course.objects.get_or_create(name=name)[0]
            for name in course_names
        }

    def create_class_sessions(self, courses, teachers):
        session_data = [
            ('کلاس پیانو', 'سارا کریمی', Weekday.SATURDAY, time(9, 0), time(10, 0), 8),
            ('کلاس گیتار', 'رضا مرادی', Weekday.SATURDAY, time(10, 0), time(11, 0), 10),
            ('کلاس ویولن', 'نگار احمدی', Weekday.SUNDAY, time(9, 0), time(10, 0), 6),
            ('کلاس آواز', 'نگار احمدی', Weekday.MONDAY, time(11, 0), time(12, 0), 8),
            ('کلاس پیانو', 'سارا کریمی', Weekday.WEDNESDAY, time(16, 0), time(17, 0), 8),
        ]

        for course_name, teacher_name, weekday, start_time, end_time, capacity in session_data:
            ClassSession.objects.update_or_create(
                course=courses[course_name],
                teacher=teachers[teacher_name],
                weekday=weekday,
                start_time=start_time,
                defaults={
                    'end_time': end_time,
                    'capacity': capacity,
                    'is_active': True,
                    'notes': '',
                },
            )

    def ensure_teacher_image(self, teacher, color):
        if teacher.profile_image:
            return

        image = Image.new('RGB', (400, 400), color)
        draw = ImageDraw.Draw(image)
        initials = f'{teacher.first_name[0]}{teacher.last_name[0]}'
        draw.text((170, 180), initials, fill='white')

        image_buffer = BytesIO()
        image.save(image_buffer, format='JPEG')
        teacher.profile_image.save(
            f'teacher-{teacher.pk}.jpg',
            ContentFile(image_buffer.getvalue()),
            save=True,
        )
