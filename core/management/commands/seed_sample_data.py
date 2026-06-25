from datetime import time
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw

from gallery.models import GalleryImage, GalleryPage
from schedules.models import ClassSession, Weekday
from teachers.models import Instrument, Teacher


class Command(BaseCommand):
    help = 'Create sample music academy data for local development.'

    def handle(self, *args, **options):
        instruments = self.create_instruments()
        teachers = self.create_teachers(instruments)
        self.create_class_sessions(instruments, teachers)
        self.create_gallery_sample_data()

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
                'biography': 'مدرس پیانو با تمرکز بر تکنیک، سلفژ و اجرای کلاسیک.',
                'display_order': 1,
                'image_color': '#6A8D73',
            },
            {
                'first_name': 'رضا',
                'last_name': 'مرادی',
                'instruments': ['گیتار'],
                'biography': 'مدرس گیتار کلاسیک و پاپ با تجربه اجرای صحنه‌ای.',
                'display_order': 2,
                'image_color': '#8E6C88',
            },
            {
                'first_name': 'نگار',
                'last_name': 'احمدی',
                'instruments': ['ویولن', 'آواز'],
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

    def create_class_sessions(self, instruments, teachers):
        session_data = [
            ('سارا کریمی', ['پیانو'], Weekday.SATURDAY, time(9, 0), time(10, 0)),
            ('رضا مرادی', ['گیتار'], Weekday.SATURDAY, time(10, 0), time(11, 0)),
            ('نگار احمدی', ['ویولن', 'آواز'], Weekday.SUNDAY, time(9, 0), time(10, 0)),
            ('نگار احمدی', ['آواز'], Weekday.MONDAY, time(11, 0), time(12, 0)),
            ('سارا کریمی', ['پیانو'], Weekday.WEDNESDAY, time(16, 0), time(17, 0)),
        ]

        for teacher_name, instrument_names, weekday, start_time, end_time in session_data:
            session, _ = ClassSession.objects.update_or_create(
                teacher=teachers[teacher_name],
                weekday=weekday,
                start_time=start_time,
                defaults={
                    'end_time': end_time,
                    'is_active': True,
                    'notes': '',
                },
            )
            session.instruments.set(instruments[name] for name in instrument_names)

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

    def create_gallery_sample_data(self):
        page_data = [
            {
                'title': 'گالری تصاویر',
                'slug': 'gallery-root',
                'parent': None,
                'description': 'نمونه ساختار اولیه برای گالری سایت.',
                'intro_text': 'این بخش شامل پوشه‌های نمونه برای شروع مدیریت گالری است.',
                'display_order': 1,
                'cover_color': '#7D2A1D',
            },
            {
                'title': 'کنسرت‌های آموزشگاه',
                'slug': 'academy-concerts',
                'parent_slug': 'gallery-root',
                'description': 'تصاویر اجراها و برنامه‌های داخلی آموزشگاه.',
                'intro_text': 'عکس‌های مربوط به اجراهای هنرجویان و اساتید.',
                'display_order': 1,
                'cover_color': '#A14A28',
            },
            {
                'title': 'کنسرت سال ۱۴۰۴',
                'slug': 'concert-1404',
                'parent_slug': 'academy-concerts',
                'description': 'تصاویر منتخب از کنسرت سال ۱۴۰۴.',
                'intro_text': 'نمونه‌ای از تصاویر رویداد سال ۱۴۰۴.',
                'display_order': 1,
                'cover_color': '#C76C3A',
            },
            {
                'title': 'آموزشگاه و متفرقه',
                'slug': 'academy-misc',
                'parent_slug': 'gallery-root',
                'description': 'تصاویر محیط آموزشگاه و برنامه‌های عمومی.',
                'intro_text': 'عکس‌هایی از کلاس‌ها، محیط و رویدادهای غیررسمی.',
                'display_order': 2,
                'cover_color': '#546A7B',
            },
            {
                'title': 'فضای آموزشگاه',
                'slug': 'academy-space',
                'parent': None,
                'description': 'تصاویر فضای فیزیکی و کلاس‌های آموزشگاه برای صفحه درباره ما.',
                'intro_text': 'نمایی از محیط آموزشی و کلاس‌های آموزشگاه.',
                'display_order': 3,
                'cover_color': '#3F5E5A',
            },
        ]

        pages_by_slug = {}
        for data in page_data:
            cover_color = data.pop('cover_color')
            parent_slug = data.pop('parent_slug', None)
            parent = pages_by_slug.get(parent_slug) if parent_slug else None
            page, _ = GalleryPage.objects.update_or_create(
                slug=data['slug'],
                parent=parent,
                defaults={
                    'title': data['title'],
                    'description': data['description'],
                    'intro_text': data['intro_text'],
                    'display_order': data['display_order'],
                    'is_active': True,
                },
            )
            self.ensure_gallery_cover_image(page, cover_color)
            pages_by_slug[data['slug']] = page

        image_data = [
            {
                'page_slug': 'concert-1404',
                'title': 'اجرای گروهی هنرجویان',
                'caption': 'نمونه تصویر برای اجرای گروهی در سالن آموزشگاه.',
                'display_order': 1,
                'color': '#C08457',
            },
            {
                'page_slug': 'concert-1404',
                'title': 'پشت صحنه کنسرت',
                'caption': 'آماده‌سازی هنرجویان قبل از اجرا.',
                'display_order': 2,
                'color': '#8E6C88',
            },
            {
                'page_slug': 'academy-misc',
                'title': 'فضای کلاس پیانو',
                'caption': 'نمونه تصویر از فضای داخلی کلاس‌ها.',
                'display_order': 1,
                'color': '#6A8D73',
            },
            {
                'page_slug': 'academy-space',
                'title': 'سالن تمرین',
                'caption': 'نمونه تصویر از سالن تمرین آموزشگاه.',
                'display_order': 1,
                'color': '#3F5E5A',
            },
            {
                'page_slug': 'academy-space',
                'title': 'اتاق کلاس',
                'caption': 'نمونه تصویر از اتاق کلاس‌های خصوصی.',
                'display_order': 2,
                'color': '#7D6B57',
            },
        ]

        for data in image_data:
            page = pages_by_slug[data['page_slug']]
            image, _ = GalleryImage.objects.get_or_create(
                gallery_page=page,
                title=data['title'],
                defaults={
                    'caption': data['caption'],
                    'display_order': data['display_order'],
                    'is_active': True,
                },
            )
            image.caption = data['caption']
            image.display_order = data['display_order']
            image.is_active = True
            self.ensure_gallery_image_file(image, data['color'])

    def ensure_gallery_cover_image(self, page, color):
        if page.cover_image:
            return

        image_buffer = self.build_labeled_image(page.title, color, size=(960, 420))
        page.cover_image.save(
            f'gallery-cover-{page.slug}.jpg',
            ContentFile(image_buffer.getvalue()),
            save=True,
        )

    def ensure_gallery_image_file(self, image, color):
        if image.image:
            image.save(update_fields=['caption', 'display_order', 'is_active', 'updated_at'])
            return

        label = image.title or image.gallery_page.title
        image_buffer = self.build_labeled_image(label, color, size=(960, 640))
        image.image.save(
            f'gallery-image-{image.gallery_page.slug}-{image.display_order}.jpg',
            ContentFile(image_buffer.getvalue()),
            save=True,
        )

    def build_labeled_image(self, label, color, size):
        image = Image.new('RGB', size, color)
        draw = ImageDraw.Draw(image)
        short_label = label[:24]
        draw.text((40, 40), short_label, fill='white')
        image_buffer = BytesIO()
        image.save(image_buffer, format='JPEG')
        return image_buffer
