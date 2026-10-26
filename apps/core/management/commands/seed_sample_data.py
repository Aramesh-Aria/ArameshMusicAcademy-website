import json
from datetime import time
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand

from apps.gallery.models import GalleryImage, GalleryPage
from apps.pages.models import SitePageContent
from apps.programmes.models import Programme
from apps.schedules.models import ClassSession
from apps.teachers.models import Instrument, Teacher

# Content and photos taken from the live site (aramesh-academy.ir), so local development shows the real academy.
DATA_DIR = Path(__file__).resolve().parent / 'seed_data'


class Command(BaseCommand):
    help = (
        'Fill the database with the academy\'s real content (Programmes, Instruments, teachers, sessions, gallery, '
        'About text and the home page\'s teaching sections) for local development.'
    )

    def handle(self, *args, **options):
        with open(DATA_DIR / 'academy.json', encoding='utf-8') as f:
            data = json.load(f)

        programmes = self.create_programmes(data['programmes'])
        instruments = self.create_instruments(data['instruments'])
        self.create_teachers(data['teachers'], instruments, programmes)
        self.create_gallery(data['gallery_pages'])
        self.create_about_page(data['about'])
        self.create_sections(data['sections'])

        self.stdout.write(self.style.SUCCESS('Academy data is ready.'))

    def create_programmes(self, programme_data):
        # get_or_create, so copy edited in the admin survives a re-run.
        programmes = {}
        for data in programme_data:
            fields = dict(data)
            name = fields.pop('name')
            programmes[name] = Programme.objects.get_or_create(name=name, defaults=fields)[0]
        return programmes

    def create_instruments(self, instrument_data):
        instruments = {}
        for data in instrument_data:
            fields = dict(data)
            name = fields.pop('name')
            instruments[name] = Instrument.objects.update_or_create(name=name, defaults=fields)[0]
        return instruments

    def create_teachers(self, teacher_data, instruments, programmes):
        for data in teacher_data:
            teacher, _ = Teacher.objects.update_or_create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                defaults={
                    'biography': data['biography'],
                    'lineage': data['lineage'],
                    'display_order': data['display_order'],
                    'is_active': True,
                },
            )
            teacher.instruments.set(instruments[name] for name in data['instruments'])
            teacher.programmes.set(programmes[name] for name in data['programmes'])
            self.ensure_teacher_image(teacher, data['image'])

            for session_data in data['sessions']:
                session, _ = ClassSession.objects.update_or_create(
                    teacher=teacher,
                    weekday=session_data['weekday'],
                    start_time=time.fromisoformat(session_data['start']),
                    defaults={
                        'end_time': time.fromisoformat(session_data['end']),
                        # A session reserved for a fixed-time Programme, such as Thursday's ensemble playing.
                        'programme': programmes.get(session_data.get('programme')),
                        'is_active': True,
                        'notes': '',
                    },
                )
                session.instruments.set(instruments[name] for name in session_data['instruments'])

    def ensure_teacher_image(self, teacher, image_path):
        if teacher.profile_image:
            return

        # A few teachers have no photo on the live site. They keep none, so the site shows its designed
        # fallback (initials on a stone plate) rather than a made-up picture.
        if image_path is None:
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

    def create_sections(self, sections):
        # The home page's «how we teach» and «three steps» sections, also editable in the admin.
        for page_key, content in sections.items():
            SitePageContent.objects.get_or_create(
                page_key=page_key,
                defaults={'title': content['title'], 'body': content['body'], 'is_active': True},
            )

    def save_seed_file(self, field_file, relative_path):
        # Saving through the field runs the model's save(), which resizes and crops the upload.
        path = DATA_DIR / 'images' / relative_path
        with open(path, 'rb') as f:
            field_file.save(path.name, File(f), save=True)
