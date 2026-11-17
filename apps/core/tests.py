import os
import shutil
import tempfile
import time
from io import BytesIO, StringIO
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import Client, RequestFactory, TestCase, override_settings
from django.urls import reverse

from apps.gallery.models import GalleryImage, GalleryPage
from apps.pages.models import SitePageContent
from apps.programmes.models import Programme
from apps.teachers.models import Instrument, Teacher

from PIL import Image

from . import image_utils
from .image_utils import image_sizes, make_image_sizes, wait_for_image_sizes
from .templatetags.site_tags import fa_digits, image_size, local_phone, srcset, tel_href
from .views import server_error


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

        # The stored photo is WebP itself, so it is its own 600px copy.
        stem = os.path.splitext(teacher.profile_image.name)[0]
        self.assertEqual(self._copies(), [f'{stem}-{width}w.webp' for width in (320, 480)])
        self.assertEqual(image_sizes(teacher.profile_image)[-1], (teacher.profile_image.url, 600))

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


class ServerErrorPageTests(TestCase):
    def test_the_site_500_handler_is_installed(self):
        from config import urls

        self.assertEqual(urls.handler500, 'apps.core.views.server_error')

    def test_server_error_page_gives_the_phone_without_touching_the_database(self):
        with self.assertNumQueries(0):
            response = server_error(RequestFactory().get('/'))

        self.assertEqual(response.status_code, 500)
        self.assertContains(response, 'مشکلی پیش آمد', status_code=500)
        self.assertContains(response, 'href="tel:+982144457748"', status_code=500)

    def test_a_server_error_page_that_cannot_render_still_answers_500(self):
        with patch('apps.core.views.loader.get_template', side_effect=RuntimeError), self.assertLogs('apps.core.views', 'ERROR'):
            response = server_error(RequestFactory().get('/'))

        self.assertEqual(response.status_code, 500)
        self.assertContains(response, 'Server Error (500)', status_code=500)


class ExpiredFormPageTests(TestCase):
    def test_a_form_sent_without_its_csrf_cookie_gets_the_persian_page_with_the_form_link(self):
        response = Client(enforce_csrf_checks=True).post(reverse('contact:contact'), {'full_name': 'x', 'phone': '09120000000'})

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403_csrf.html')
        self.assertContains(response, 'فرم منقضی شد', status_code=403)
        self.assertContains(response, f'href="{reverse("contact:contact")}"', status_code=403)

    def test_a_form_of_the_admin_sent_without_its_csrf_cookie_points_back_to_the_admin(self):
        response = Client(enforce_csrf_checks=True).post(reverse('admin:login'), {'username': 'x', 'password': 'x'})

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403_csrf.html')
        self.assertContains(response, f'href="{reverse("admin:index")}"', status_code=403)
        self.assertNotContains(response, 'پیام شما فرستاده نشد', status_code=403)


class ForbiddenPageTests(TestCase):
    def test_a_staff_account_without_permission_gets_the_persian_403_with_the_way_back_to_the_admin(self):
        from django.contrib.auth import get_user_model

        user = get_user_model().objects.create_user('staff', password='x', is_staff=True)
        self.client.force_login(user)

        response = self.client.get(reverse('admin:teachers_teacher_changelist'))

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')
        self.assertContains(response, 'اجازهٔ دیدن این صفحه را ندارید', status_code=403)
        self.assertContains(response, f'href="{reverse("admin:index")}"', status_code=403)


class BadRequestPageTests(TestCase):
    def test_the_site_400_handler_is_installed(self):
        from config import urls

        self.assertEqual(urls.handler400, 'apps.core.views.bad_request')

    @override_settings(ALLOWED_HOSTS=['aramesh-academy.ir'])
    def test_a_request_for_a_host_that_is_not_ours_gets_the_persian_400_without_touching_the_database(self):
        with self.assertNumQueries(0), self.assertLogs('django.security.DisallowedHost', 'ERROR'):
            response = self.client.get('/', HTTP_HOST='bad.example')

        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'این درخواست درست نرسید', status_code=400)
        self.assertContains(response, 'href="tel:+982144457748"', status_code=400)


def _upload(name='a.jpg', size=400, colour='tan'):
    buffer = BytesIO()
    Image.new('RGB', (size, size), colour).save(buffer, 'JPEG')
    return SimpleUploadedFile(name, buffer.getvalue(), content_type='image/jpeg')


class StoredAsWebpTests(MediaRootMixin, TestCase):
    def _teacher(self, **kwargs):
        return Teacher.objects.create(first_name='علی', last_name='شمس', biography='.', **kwargs)

    def _files(self):
        return sorted(
            os.path.relpath(os.path.join(folder, name), self.media)
            for folder, _, names in os.walk(self.media) for name in names
        )

    def test_an_uploaded_jpeg_is_stored_as_webp_and_the_jpeg_is_gone(self):
        teacher = self._teacher(profile_image=_upload('portrait.jpg', 900))

        self.assertEqual(teacher.profile_image.name, 'teachers/portrait.webp')
        self.assertEqual(self._files(), ['teachers/portrait.webp'])
        with Image.open(teacher.profile_image.path) as stored:
            self.assertEqual((stored.format, stored.size), ('WEBP', (600, 600)))
        self.assertEqual(Teacher.objects.get(pk=teacher.pk).profile_image.name, 'teachers/portrait.webp')

    def test_a_second_upload_with_the_same_file_name_does_not_overwrite_the_first(self):
        first = self._teacher(profile_image=_upload('portrait.jpg', colour='red'))
        second = self._teacher(profile_image=_upload('portrait.jpg', colour='blue'))

        self.assertNotEqual(first.profile_image.name, second.profile_image.name)
        with Image.open(first.profile_image.path) as stored:
            red, _, blue = stored.convert('RGB').getpixel((10, 10))
        self.assertGreater(red, blue)

    def test_a_link_preview_of_a_webp_upload_says_it_is_webp(self):
        teacher = self._teacher(profile_image=_upload())

        response = self.client.get(reverse('teachers:teacher_detail', args=[teacher.pk]))

        self.assertContains(response, '<meta property="og:image:type" content="image/webp">', html=True)


class ReplacedUploadsTests(MediaRootMixin, TestCase):
    def _teacher(self, **kwargs):
        return Teacher.objects.create(first_name='علی', last_name='شمس', biography='.', **kwargs)

    def _exists(self, name):
        return os.path.exists(os.path.join(self.media, name))

    def _with_copies(self, teacher):
        make_image_sizes(teacher.profile_image)
        copy = f'sizes/{os.path.splitext(teacher.profile_image.name)[0]}-320w.webp'
        self.assertTrue(self._exists(copy))
        return teacher.profile_image.name, copy

    def test_replacing_a_photo_removes_the_old_file_and_its_copies_once_the_save_commits(self):
        teacher = self._teacher(profile_image=_upload('old.jpg'))
        old, old_copy = self._with_copies(teacher)

        with patch('apps.core.image_utils._enqueue'), self.captureOnCommitCallbacks(execute=True):
            teacher.profile_image = _upload('new.jpg')
            teacher.save()
            self.assertTrue(self._exists(old))  # not before the commit: a rolled-back save keeps its photo

        self.assertFalse(self._exists(old))
        self.assertFalse(self._exists(old_copy))
        self.assertTrue(self._exists(teacher.profile_image.name))

    def test_saving_a_row_without_touching_its_photo_keeps_the_photo(self):
        teacher = self._teacher(profile_image=_upload())

        with self.captureOnCommitCallbacks(execute=True):
            teacher.first_name = 'رضا'
            teacher.save()

        self.assertTrue(self._exists(teacher.profile_image.name))

    def test_clearing_an_optional_photo_removes_its_file(self):
        instrument = Instrument.objects.create(name='سنتور', slug='santur', photo=_upload())
        name = instrument.photo.name

        with self.captureOnCommitCallbacks(execute=True):
            instrument.photo = ''
            instrument.save()

        self.assertFalse(self._exists(name))

    def test_deleting_a_row_removes_its_file_and_copies(self):
        teacher = self._teacher(profile_image=_upload())
        name, copy = self._with_copies(teacher)

        with self.captureOnCommitCallbacks(execute=True):
            teacher.delete()

        self.assertFalse(self._exists(name))
        self.assertFalse(self._exists(copy))

    def test_deleting_a_gallery_page_removes_the_files_of_its_images(self):
        page = GalleryPage.objects.create(title='کنسرت', slug='concerts')
        image = GalleryImage.objects.create(gallery_page=page, image=_upload())

        with self.captureOnCommitCallbacks(execute=True):
            page.delete()

        self.assertFalse(self._exists(image.image.name))

    def test_a_file_another_row_still_names_is_kept(self):
        first = self._teacher(profile_image=_upload())
        self._teacher(profile_image=first.profile_image.name)

        with self.captureOnCommitCallbacks(execute=True):
            first.delete()

        self.assertTrue(self._exists(first.profile_image.name))

    def test_a_copy_of_a_longer_named_photo_is_not_taken_for_this_ones(self):
        teacher = self._teacher(profile_image=_upload('a.jpg'))
        other = self._teacher(profile_image=_upload('a-1.jpg'))
        _, other_copy = self._with_copies(other)

        with self.captureOnCommitCallbacks(execute=True):
            teacher.delete()

        self.assertTrue(self._exists(other_copy))


class CleanMediaCommandTests(MediaRootMixin, TestCase):
    def _old_file(self, name, age=2 * 60 * 60):
        path = os.path.join(self.media, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(b'x' * 2048)
        os.utime(path, (time.time() - age,) * 2)
        return path

    def _run(self, *args):
        out = StringIO()
        call_command('clean_media', *args, stdout=out)
        return out.getvalue()

    def setUp(self):
        super().setUp()
        self.teacher = Teacher.objects.create(first_name='علی', last_name='شمس', biography='.', profile_image=_upload('kept.jpg'))
        make_image_sizes(self.teacher.profile_image)
        self.kept = self.teacher.profile_image.path
        self.kept_copy = os.path.join(self.media, 'sizes/teachers/kept-320w.webp')
        for path in (self.kept, self.kept_copy):
            os.utime(path, (time.time() - 7200,) * 2)
        self.orphan = self._old_file('teachers/replaced.jpg')
        self.orphan_copy = self._old_file('sizes/teachers/replaced-320w.webp')

    def test_it_only_lists_unless_told_to_delete(self):
        out = self._run()

        self.assertIn('teachers/replaced.jpg', out)
        self.assertIn('sizes/teachers/replaced-320w.webp', out)
        self.assertNotIn('kept', out)
        self.assertIn('2 unused files', out)
        self.assertIn('Nothing was removed', out)
        self.assertTrue(os.path.exists(self.orphan))

    def test_delete_removes_unused_files_and_keeps_photos_in_use_with_their_copies(self):
        self._run('--delete')

        self.assertFalse(os.path.exists(self.orphan))
        self.assertFalse(os.path.exists(self.orphan_copy))
        self.assertTrue(os.path.exists(self.kept))
        self.assertTrue(os.path.exists(self.kept_copy))

    def test_a_file_changed_in_the_last_hour_is_left_alone(self):
        fresh = self._old_file('gallery/uploading.jpg', age=60)

        out = self._run('--delete')

        self.assertTrue(os.path.exists(fresh))
        self.assertIn('1 unused files changed in the last hour', out)

    def test_it_refuses_to_delete_when_the_database_names_no_file_at_all(self):
        from django.core.management.base import CommandError

        Teacher.objects.all().delete()
        self._old_file('teachers/kept.webp')

        with self.assertRaises(CommandError):
            self._run('--delete')
        self.assertTrue(os.path.exists(self.orphan))

    def test_a_file_outside_the_upload_folders_is_never_touched(self):
        other = self._old_file('backups/db.sqlite3')

        out = self._run('--delete')

        self.assertTrue(os.path.exists(other))
        self.assertIn('1 files outside the upload folders were not looked at', out)


class ConvertMediaToWebpCommandTests(MediaRootMixin, TestCase):
    def _jpeg(self, name, size=900):
        path = os.path.join(self.media, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        Image.effect_noise((size, size), 60).convert('RGB').save(path, 'JPEG', quality=95)
        return name

    def _teacher(self, name):
        teacher = Teacher(first_name='علی', last_name='شمس', biography='.')
        teacher.save()
        Teacher.objects.filter(pk=teacher.pk).update(profile_image=name)  # as a photo stored before WebP
        return teacher

    def _exists(self, name):
        return os.path.exists(os.path.join(self.media, name))

    def _run(self, *args):
        out, err = StringIO(), StringIO()
        call_command('convert_media_to_webp', *args, stdout=out, stderr=err)
        return out.getvalue(), err.getvalue()

    def test_it_only_lists_unless_told_to_convert(self):
        teacher = self._teacher(self._jpeg('teachers/old.jpg'))

        out, _ = self._run()

        self.assertIn('teachers/old.jpg:', out)
        self.assertIn('Nothing was changed', out)
        self.assertEqual(os.listdir(os.path.join(self.media, 'teachers')), ['old.jpg'])
        self.assertEqual(Teacher.objects.get(pk=teacher.pk).profile_image.name, 'teachers/old.jpg')

    def test_convert_stores_the_photo_as_webp_at_the_same_size_and_removes_the_jpeg_and_its_copies(self):
        teacher = self._teacher(self._jpeg('teachers/old.jpg'))
        make_image_sizes(Teacher.objects.get(pk=teacher.pk).profile_image)
        self.assertTrue(self._exists('sizes/teachers/old-900w.webp'))

        out, _ = self._run('--convert')

        photo = Teacher.objects.get(pk=teacher.pk).profile_image
        self.assertEqual(photo.name, 'teachers/old.webp')
        with Image.open(photo.path) as stored:
            self.assertEqual((stored.format, stored.size), ('WEBP', (900, 900)))
        self.assertFalse(self._exists('teachers/old.jpg'))
        self.assertFalse(self._exists('sizes/teachers/old-900w.webp'))
        self.assertEqual([width for _, width in image_sizes(photo)], [320, 480, 800, 900])
        self.assertIn('1 photos', out)
        self.assertIn('Converted', out)

    def test_every_row_that_named_the_jpeg_names_the_webp(self):
        name = self._jpeg('teachers/shared.jpg')
        first, second = self._teacher(name), self._teacher(name)

        self._run('--convert')

        names = set(Teacher.objects.filter(pk__in=[first.pk, second.pk]).values_list('profile_image', flat=True))
        self.assertEqual(names, {'teachers/shared.webp'})

    def test_a_webp_name_already_taken_is_not_overwritten(self):
        self._teacher(self._jpeg('teachers/a.jpg'))
        taken = os.path.join(self.media, 'teachers/a.webp')
        Image.new('RGB', (10, 10), 'red').save(taken, 'WEBP')
        other = self._teacher('teachers/a.webp')

        self._run('--convert')

        with Image.open(taken) as untouched:
            self.assertEqual(untouched.size, (10, 10))
        self.assertEqual(Teacher.objects.get(pk=other.pk).profile_image.name, 'teachers/a.webp')

    def test_a_missing_photo_is_reported_and_the_rest_are_converted(self):
        self._teacher('teachers/gone.jpg')
        kept = self._teacher(self._jpeg('teachers/here.jpg'))

        out, err = self._run('--convert')

        self.assertIn('teachers/gone.jpg: could not be read', err)
        self.assertEqual(Teacher.objects.get(pk=kept.pk).profile_image.name, 'teachers/here.webp')
        self.assertIn('Could not read 1', out)

    def test_a_photo_whose_webp_would_not_be_lighter_is_left_as_it_is(self):
        teacher = self._teacher(self._jpeg('teachers/tiny.jpg'))

        with patch('apps.core.management.commands.convert_media_to_webp.os.path.getsize', return_value=1):
            out, _ = self._run('--convert')

        self.assertIn('left as it is', out)
        self.assertEqual(Teacher.objects.get(pk=teacher.pk).profile_image.name, 'teachers/tiny.jpg')
        self.assertEqual(os.listdir(os.path.join(self.media, 'teachers')), ['tiny.jpg'])
