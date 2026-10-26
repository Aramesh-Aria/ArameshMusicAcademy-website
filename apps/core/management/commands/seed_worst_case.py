from datetime import time

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from apps.gallery.models import GalleryPage
from apps.pages.models import FAQ
from apps.programmes.models import Programme
from apps.schedules.models import ClassSession
from apps.teachers.models import Instrument, Teacher
from apps.testimonials.models import Testimonial


class Command(BaseCommand):
    help = (
        'Development only: load the real academy data, then push it to the realistic worst case (long Persian '
        'names at their real limits, a teacher with six Instruments, one testimonial, one long FAQ, an empty '
        'gallery sub-page). Run it against a separate database: DATABASE_PATH=database/worst.sqlite3.'
    )

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError('This command rewrites content for testing; run it with DEBUG=True.')
        if str(settings.DATABASES['default']['NAME']).endswith('database/db.sqlite3'):
            raise CommandError('Point DATABASE_PATH at a separate database first, e.g. database/worst.sqlite3.')

        call_command('seed_sample_data', stdout=self.stdout)

        # The brief's case: Ali Shams with six Instruments, a «.» biography and no portrait, here teaching six days.
        ali = Teacher.objects.get(first_name='علی', last_name='شمس')
        ali.instruments.add(Instrument.objects.get(name='فلوت'))
        for weekday in ['sat', 'sun', 'mon', 'tue', 'wed', 'thu']:
            session = ClassSession.objects.create(teacher=ali, weekday=weekday, start_time=time(8), end_time=time(9, 30))
            session.instruments.set(ali.instruments.all())

        # A long but ordinary Persian name, with a lineage line at its 120-character limit.
        teacher = Teacher.objects.get(first_name='علیرضا', last_name='مهدیزاده')
        teacher.first_name = 'سیدمحمدحسین'
        teacher.last_name = 'میرهاشمی طباطبایی‌نژاد'
        teacher.lineage = (
            'آموخته نزد محمدرضا شجریان، شاپور رحیمی و پری ملکی؛ کارشناسی ارشد موسیقی ایرانی از دانشگاه هنر تهران'
        )[:120]
        teacher.save()

        # An Instrument whose name runs to two lines in a tile.
        Instrument.objects.create(name='سازهای کوبه‌ای آفریقایی و آمریکای لاتین', slug='world-percussion')

        # A Programme with a long name and an age label at its 40-character limit.
        programme = Programme.objects.get(slug='children')
        programme.name = 'آموزش موسیقی کودک به روش ارف، ویژهٔ پیش‌دبستانی'
        programme.age_label = 'از ۴ تا ۶ سال، همراه با یکی از والدین'
        programme.save()

        # An empty sub-page under an empty album, titled the way a concert gets written up.
        concerts = GalleryPage.objects.get(slug='concerts')
        GalleryPage.objects.create(
            parent=concerts,
            slug='spring-recital',
            title='کنسرت پایانی هنرجویان سنتور و آواز ایرانی در تالار وحدت، بهار ۱۴۰۳',
        )

        # One testimonial (a marquee of one) with a long relation line, and one long FAQ.
        Testimonial.objects.create(
            author_name='فاطمه‌سادات حسینی‌طباطبایی',
            relation='مادر دو هنرجوی پیانو و سنتور، از سال ۱۳۹۸ در آموزشگاه',
            quote='دخترم از هفت سالگی اینجا پیانو می‌زند و پسرم پارسال سنتور را شروع کرد. استادها صبورند و '
                  'هر جلسه چیزی تازه با خودشان به خانه می‌آورند.',
        )
        faq = FAQ.objects.create(
            question='اگر فرزندم پیش از این هیچ سازی نزده و هنوز نمی‌دانیم کدام ساز برایش مناسب است، '
                     'از کجا شروع کنیم و جلسهٔ اول چطور می‌گذرد؟',
            answer='با آموزشگاه تماس بگیرید تا با هم یک جلسهٔ آشنایی بگذاریم.\n\n'
                   'در این جلسه کودک چند ساز را از نزدیک می‌بیند و امتحان می‌کند.',
        )
        faq.programmes.add(programme)

        self.stdout.write(self.style.SUCCESS('Worst-case data is ready.'))
