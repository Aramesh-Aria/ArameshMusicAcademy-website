import os
import shutil
import tempfile
import time
from io import BytesIO, StringIO
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse

from apps.gallery.models import GalleryImage, GalleryPage
from apps.pages.models import SitePageContent
from apps.programmes.models import Programme
from apps.teachers.models import Instrument, Teacher

from PIL import Image

from . import image_utils
from .image_utils import image_sizes, make_image_sizes, wait_for_image_sizes
from .templatetags.site_tags import fa_digits, image_size, local_phone, srcset, tel_href


def _jpeg_bytes(width, height):
    buffer = BytesIO()
    Image.new('RGB', (width, height), 'tan').save(buffer, 'JPEG')
    return buffer.getvalue()


class PhoneFilterTests(TestCase):
    def test_local_phone_shows_an_international_landline_in_local_form(self):
        self.assertEqual(local_phone('+98 21 4445 7748'), '021 4445 7748')

    def test_local_phone_shows_an_international_mobile_in_local_form(self):
        self.assertEqual(local_phone('+98 990 233 8431'), '0990 233 8431')

    def test_local_phone_leaves_a_local_number_alone(self):
        self.assertEqual(local_phone('021 4445 7748'), '021 4445 7748')

    def test_fa_digits_turns_ascii_digits_persian_and_leaves_the_rest(self):
        self.assertEqual(fa_digits('ساعت 14:30، 1404'), 'ساعت ۱۴:۳۰، ۱۴۰۴')
        self.assertEqual(fa_digits(404), '۴۰۴')

    def test_tel_href_strips_spaces_and_keeps_the_country_code(self):
        self.assertEqual(tel_href('+98 21 4445 7748'), 'tel:+982144457748')


class ImageSizeTagTests(TestCase):
    def test_image_size_gives_the_files_width_and_height(self):
        class Field:
            width, height = 900, 1200
        self.assertEqual(image_size(Field()), 'width="900" height="1200"')

    def test_image_size_is_empty_when_the_file_is_missing(self):
        class Missing:
            @property
            def width(self):
                raise FileNotFoundError('gallery/gone.jpg')
        self.assertEqual(image_size(Missing()), '')



class MediaRootMixin:
    def setUp(self):
        super().setUp()
        self.media = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.media)
        override = override_settings(MEDIA_ROOT=self.media)
        override.enable()
        self.addCleanup(override.disable)

    def _photo(self, width, height=None, name='teachers/a.jpg'):
        path = os.path.join(self.media, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        Image.new('RGB', (width, height or width), 'tan').save(path, 'JPEG')
        return name

    def _portrait(self, width, height=None, name='teachers/a.jpg'):
        return Teacher(profile_image=self._photo(width, height, name)).profile_image

    def _broken(self, name='teachers/broken.jpg'):
        path = os.path.join(self.media, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(b'not a photo')
        return name

    def _copies(self):
        sizes = os.path.join(self.media, 'sizes')
        return sorted(
            os.path.relpath(os.path.join(root, name), sizes) for root, _, names in os.walk(sizes) for name in names
        )


class SrcsetTests(MediaRootMixin, TestCase):
    """Smaller WebP copies of an upload, made after it is saved, so a phone isn't sent the 1920px photo."""

    def test_copies_go_up_to_the_originals_own_width(self):
        field = self._portrait(600)
        self.assertEqual(make_image_sizes(field), 3)

        sizes = image_sizes(field)

        self.assertEqual([width for _, width in sizes], [320, 480, 600])
        self.assertEqual(sizes[0][0], '/public/media/sizes/teachers/a-320w.webp')
        with Image.open(os.path.join(self.media, 'sizes/teachers/a-480w.webp')) as copy:
            self.assertEqual((copy.format, copy.size), ('WEBP', (480, 480)))

    def test_a_narrow_upload_is_offered_at_its_own_width_only(self):
        field = self._portrait(300)
        make_image_sizes(field)
        self.assertEqual([width for _, width in image_sizes(field)], [300])

    def test_offering_copies_never_makes_one(self):
        field = self._portrait(600)

        self.assertEqual(image_sizes(field), [])
        self.assertEqual(srcset(field, '50vw'), '')
        self.assertEqual(self._copies(), [])

    def test_a_stale_or_missing_copy_is_left_out_and_the_original_stands_in_at_full_width(self):
        field = self._portrait(600)
        make_image_sizes(field)
        os.utime(os.path.join(self.media, 'sizes/teachers/a-480w.webp'), (0, 0))  # the admin replaced the photo
        os.remove(os.path.join(self.media, 'sizes/teachers/a-600w.webp'))

        self.assertEqual(image_sizes(field), [
            ('/public/media/sizes/teachers/a-320w.webp', 320),
            ('/public/media/teachers/a.jpg', 600),
        ])

    def test_a_replaced_photo_gets_new_copies_and_fresh_ones_are_kept(self):
        field = self._portrait(600)
        make_image_sizes(field)
        stale = os.path.join(self.media, 'sizes/teachers/a-320w.webp')
        os.utime(stale, (0, 0))  # older than the original, as when the admin uploads over the same name

        self.assertEqual(make_image_sizes(field), 1)
        self.assertGreater(os.path.getmtime(stale), 0)
        self.assertEqual(make_image_sizes(field), 0)

    def test_a_large_jpeg_is_shrunk_to_each_exact_width(self):
        field = self._portrait(2400, 1600)
        make_image_sizes(field)

        for width, height in ((320, 213), (1200, 800), (2400, 1600)):
            with Image.open(os.path.join(self.media, f'sizes/teachers/a-{width}w.webp')) as copy:
                self.assertEqual(copy.size, (width, height))

    def test_the_tag_names_each_copy_and_the_sizes(self):
        field = self._portrait(600)
        make_image_sizes(field)
        html = srcset(field, '50vw', 'data-srcset')

        self.assertEqual(html, 'data-srcset="/public/media/sizes/teachers/a-320w.webp 320w, '
                               '/public/media/sizes/teachers/a-480w.webp 480w, '
                               '/public/media/sizes/teachers/a-600w.webp 600w" sizes="50vw"')

    def test_a_missing_or_broken_file_leaves_the_plain_src(self):
        self.assertEqual(srcset(Teacher(profile_image='teachers/gone.jpg').profile_image, '50vw'), '')
        self.assertEqual(srcset(Teacher(profile_image=self._broken()).profile_image, '50vw'), '')


class PageRenderMakesNoCopiesTests(MediaRootMixin, TestCase):
    def test_a_page_full_of_photos_with_no_copies_renders_fast_and_makes_none(self):
        page = GalleryPage.objects.create(title='کنسرت', slug='concerts')
        # bulk_create skips save(), so no copies are scheduled: the state after a lost background job.
        GalleryImage.objects.bulk_create([
            *(GalleryImage(gallery_page=page, image=self._photo(1920, 1280, f'gallery/{n}.jpg'), display_order=n)
              for n in range(30)),
            GalleryImage(gallery_page=page, image=self._broken('gallery/broken.jpg'), display_order=99),
        ])

        with patch('apps.core.image_utils.make_image_sizes', side_effect=AssertionError('made a copy')):
            start = time.monotonic()
            response = self.client.get(page.get_absolute_url())
            elapsed = time.monotonic() - start

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '/public/media/gallery/0.jpg')
        self.assertNotContains(response, 'srcset=')
        self.assertEqual(self._copies(), [])
        self.assertLess(elapsed, 2)  # making 30 photos' copies takes several seconds even here


class ScheduledCopiesTests(MediaRootMixin, TestCase):
    def test_saving_an_upload_makes_its_copies_after_commit_off_the_request(self):
        upload = SimpleUploadedFile('a.jpg', _jpeg_bytes(1000, 1000), content_type='image/jpeg')

        with self.captureOnCommitCallbacks() as callbacks:
            teacher = Teacher.objects.create(first_name='علی', last_name='شمس', biography='.', profile_image=upload)
        self.assertEqual(self._copies(), [])  # nothing made inside save()
        self.assertEqual(len(callbacks), 1)

        for callback in callbacks:
            callback()
        wait_for_image_sizes()

        stem = os.path.splitext(teacher.profile_image.name)[0]
        self.assertEqual(self._copies(), [f'{stem}-{width}w.webp' for width in (320, 480, 600)])

    def test_every_model_that_processes_an_upload_schedules_its_copies(self):
        def upload():
            return SimpleUploadedFile('p.jpg', _jpeg_bytes(400, 400), content_type='image/jpeg')

        page = GalleryPage.objects.create(title='کنسرت', slug='concerts')
        makers = {
            'GalleryPage': lambda: GalleryPage.objects.create(title='صفحه', slug='page', cover_image=upload()),
            'GalleryImage': lambda: GalleryImage.objects.create(gallery_page=page, image=upload()),
            'Instrument': lambda: Instrument.objects.create(name='سنتور', slug='santur', photo=upload()),
            'Programme': lambda: Programme.objects.create(
                name='تئوری', slug='theory', short_description='.', long_description='.',
                photo_1=upload(), photo_2=upload(),
            ),
            'SitePageContent': lambda: SitePageContent.objects.create(
                page_key=SitePageContent.HOME, title='.', body='.', hero_image=upload(),
            ),
            'Teacher': lambda: Teacher.objects.create(first_name='.', last_name='.', biography='.', profile_image=upload()),
        }
        for model, make in makers.items():
            with self.subTest(model=model), patch('apps.core.image_utils._enqueue') as enqueue:
                with self.captureOnCommitCallbacks(execute=True):
                    make()
                self.assertEqual(enqueue.call_count, 2 if model == 'Programme' else 1)

    def test_a_broken_upload_in_the_queue_does_not_stop_the_next_one(self):
        good = self._portrait(500)
        with self.assertLogs('apps.core.image_utils', 'ERROR'):
            image_utils._enqueue(Teacher(profile_image=self._broken()).profile_image)
            image_utils._enqueue(good)
            wait_for_image_sizes()

        self.assertEqual([width for _, width in image_sizes(good)], [320, 480, 500])


class MakeImageSizesCommandTests(MediaRootMixin, TestCase):
    def _run(self):
        out, err = StringIO(), StringIO()
        call_command('make_image_sizes', stdout=out, stderr=err)
        return out.getvalue(), err.getvalue()

    def test_makes_missing_copies_skips_fresh_ones_and_survives_a_broken_photo(self):
        page = GalleryPage.objects.create(title='کنسرت', slug='concerts')
        GalleryImage.objects.bulk_create([
            GalleryImage(gallery_page=page, image=self._photo(900, name='gallery/a.jpg'), display_order=1),
            GalleryImage(gallery_page=page, image=self._broken('gallery/broken.jpg'), display_order=2),
            GalleryImage(gallery_page=page, image=self._photo(300, name='gallery/b.jpg'), display_order=3),
        ])

        out, err = self._run()

        self.assertIn('gallery/a.jpg: 4 made', out)
        self.assertIn('gallery/b.jpg: 1 made', out)
        self.assertIn('5 copies made for 3 photos. Could not read 1 of them.', out)
        self.assertIn('gallery/broken.jpg: could not be read', err)
        self.assertEqual(len(self._copies()), 5)

        os.utime(os.path.join(self.media, 'sizes/gallery/a-800w.webp'), (0, 0))
        out, _ = self._run()

        self.assertIn('gallery/a.jpg: 1 made', out)
        self.assertIn('gallery/b.jpg: up to date', out)

class BaseLayoutTests(TestCase):
    def test_every_page_offers_the_primary_phone_and_the_gallery_menu(self):
        response = self.client.get(reverse('contact:contact'))

        self.assertContains(response, 'href="tel:+982144457748"')
        self.assertContains(response, '021 4445 7748')
        self.assertContains(response, 'href="%s"' % reverse('gallery:gallery_root'))

    def test_the_current_section_is_marked_in_the_navigation(self):
        response = self.client.get(reverse('teachers:teacher_list'))

        self.assertContains(response, 'aria-current="page"', count=2)  # navbar and menu

    def test_the_programmes_menu_lists_the_active_programmes_and_all_instruments(self):
        Programme.objects.create(name='تئوری و سلفژ', slug='theory', short_description='.', long_description='.')
        Programme.objects.create(
            name='دورهٔ پنهان', slug='hidden', short_description='.', long_description='.', is_active=False,
        )

        response = self.client.get(reverse('pages:about'))

        self.assertContains(response, 'href="/programmes/theory/"', count=2)  # navbar and menu
        self.assertNotContains(response, 'دورهٔ پنهان')
        self.assertContains(response, 'href="%s"' % reverse('instruments:instrument_list'))


class TemplateCommentTests(TestCase):
    def test_no_page_leaks_a_template_comment(self):
        teacher = Teacher.objects.create(first_name='علی', last_name='شمس', biography='.')
        for url in ('/', '/about/', '/teachers/', teacher.get_absolute_url(), '/schedule/', '/gallery/', '/contact/',
                    '/instruments/'):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertNotContains(response, '{#')
                self.assertNotContains(response, '#}')


class PublicDomainTests(TestCase):
    def test_canonical_og_url_and_og_image_name_the_public_domain_whichever_host_served_the_page(self):
        response = self.client.get(reverse('contact:contact'), HTTP_HOST='aramesh-academy.runflare.run')

        self.assertContains(response, '<link rel="canonical" href="https://aramesh-academy.ir/contact/">', html=True)
        self.assertContains(response, '<meta property="og:url" content="https://aramesh-academy.ir/contact/">', html=True)
        self.assertContains(response, 'property="og:image" content="https://aramesh-academy.ir/public/static/')
        self.assertNotContains(response, 'runflare.run')

    def test_the_sitemap_lists_the_public_domain_over_https_whichever_host_served_it(self):
        response = self.client.get('/sitemap.xml', HTTP_HOST='aramesh-academy.runflare.run')

        self.assertContains(response, '<loc>https://aramesh-academy.ir/</loc>')
        self.assertContains(response, '<loc>https://aramesh-academy.ir/contact/</loc>')
        self.assertNotContains(response, 'runflare.run')


class NotFoundPageTests(TestCase):
    def test_missing_page_uses_the_site_404_with_ways_back(self):
        response = self.client.get('/no-such-page/')

        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')
        self.assertContains(response, 'این صفحه در برنامه نیست', status_code=404)
        self.assertContains(response, f'href="{reverse("schedules:schedule")}"', status_code=404)
