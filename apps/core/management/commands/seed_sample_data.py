import json
from datetime import time
from io import BytesIO
from pathlib import Path

from django.core.files import File
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw

from apps.gallery.models import GalleryImage, GalleryPage
from apps.pages.models import SitePageContent
from apps.schedules.models import ClassSession
from apps.teachers.models import Instrument, Teacher

# Content and photos taken from the live site (aramesh-academy.ir), so local development shows the real academy.
DATA_DIR = Path(__file__).resolve().parent / 'seed_data'


class Command(BaseCommand):
    help = 'Fill the database with the academy\'s real content (teachers, sessions, gallery, About text) for local development.'

    def handle(self, *args, **options):
        with open(DATA_DIR / 'academy.json', encoding='utf-8') as f:
            data = json.load(f)

        instruments = self.create_instruments(data['teachers'])
        self.create_teachers(data['teachers'], instruments)
        self.create_gallery(data['gallery_pages'])
        self.create_about_page(data['about'])

        self.stdout.write(self.style.SUCCESS('Academy data is ready.'))

    def create_instruments(self, teacher_data):
        names = set()
        for teacher in teacher_data:
            names.update(teacher['instruments'])
            for session in teacher['sessions']:
                names.update(session['instruments'])
        return {name: Instrument.objects.get_or_create(name=name)[0] for name in sorted(names)}

    def create_teachers(self, teacher_data, instruments):
        for data in teacher_data:
            teacher, _ = Teacher.objects.update_or_create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                defaults={
                    'biography': data['biography'],
                    'display_order': data['display_order'],
                    'is_active': True,
                },
            )
            teacher.instruments.set(instruments[name] for name in data['instruments'])
            self.ensure_teacher_image(teacher, data['image'])

            for session_data in data['sessions']:
                session, _ = ClassSession.objects.update_or_create(
                    teacher=teacher,
                    weekday=session_data['weekday'],
                    start_time=time.fromisoformat(session_data['start']),
                    defaults={
                        'end_time': time.fromisoformat(session_data['end']),
                        'is_active': True,
                        'notes': '',
                    },
                )
                session.instruments.set(instruments[name] for name in session_data['instruments'])

    def ensure_teacher_image(self, teacher, image_path):
        if teacher.profile_image:
            return

        # A few teachers have no photo on the live site; they get a plain initials tile instead.
        if image_path is None:
            image = Image.new('RGB', (600, 600), '#3F5E5A')
            draw = ImageDraw.Draw(image)
            draw.text((285, 290), f'{teacher.first_name[0]}{teacher.last_name[0]}', fill='white')
            image_buffer = BytesIO()
            image.save(image_buffer, format='JPEG')
            teacher.profile_image.save(f'teacher-{teacher.pk}.jpg', ContentFile(image_buffer.getvalue()), save=True)
            return

        self.save_seed_file(teacher.profile_image, image_path)

    def create_gallery(self, page_data):
        for data in page_data:
            page, _ = GalleryPage.objects.update_or_create(
                slug=data['slug'],
                parent=None,
                defaults={
                    'title': data['title'],
                    'description': data['description'],
                    'display_order': data['display_order'],
                    'is_active': True,
                },
            )
            # Pages waiting for the owner's photos have no cover; GalleryPage.display_cover falls back.
            if not page.cover_image and data.get('cover_image'):
                self.save_seed_file(page.cover_image, data['cover_image'])

            for image_data in data['images']:
                image, _ = GalleryImage.objects.update_or_create(
                    gallery_page=page,
                    display_order=image_data['display_order'],
                    defaults={'title': image_data['title'], 'is_active': True},
                )
                if not image.image:
                    self.save_seed_file(image.image, image_data['image'])

    def create_about_page(self, about):
        # get_or_create, so text edited in the admin survives a re-run.
        SitePageContent.objects.get_or_create(
            page_key=SitePageContent.ABOUT,
            defaults={'title': about['title'], 'body': about['body'], 'is_active': True},
        )

    def save_seed_file(self, field_file, relative_path):
        # Saving through the field runs the model's save(), which resizes and crops the upload.
        path = DATA_DIR / 'images' / relative_path
        with open(path, 'rb') as f:
            field_file.save(path.name, File(f), save=True)
