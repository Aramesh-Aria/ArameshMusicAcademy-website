import os
import shutil
import tempfile

from django.test import TestCase, override_settings
from django.urls import reverse

from apps.programmes.models import Programme
from apps.teachers.models import Teacher

from PIL import Image

from .image_utils import image_sizes
from .templatetags.site_tags import fa_digits, image_size, local_phone, srcset, tel_href


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



class SrcsetTests(TestCase):
    """Smaller WebP copies of an upload, made on first use, so a phone isn't sent the 1920px photo."""

    def setUp(self):
        self.media = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.media)
        override = override_settings(MEDIA_ROOT=self.media)
        override.enable()
        self.addCleanup(override.disable)

    def _portrait(self, width, height=None, name='teachers/a.jpg'):
        path = os.path.join(self.media, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        Image.new('RGB', (width, height or width), 'tan').save(path, 'JPEG')
        return Teacher(profile_image=name).profile_image

    def test_copies_go_up_to_the_originals_own_width(self):
        sizes = image_sizes(self._portrait(600))

        self.assertEqual([width for _, width in sizes], [320, 480, 600])
        self.assertEqual(sizes[0][0], '/public/media/sizes/teachers/a-320w.webp')
        with Image.open(os.path.join(self.media, 'sizes/teachers/a-480w.webp')) as copy:
            self.assertEqual((copy.format, copy.size), ('WEBP', (480, 480)))

    def test_a_narrow_upload_is_offered_at_its_own_width_only(self):
        self.assertEqual([width for _, width in image_sizes(self._portrait(300))], [300])

    def test_a_replaced_photo_gets_new_copies(self):
        field = self._portrait(600)
        image_sizes(field)
        copy = os.path.join(self.media, 'sizes/teachers/a-320w.webp')
        os.utime(copy, (0, 0))  # older than the original, as when the admin uploads over the same name

        image_sizes(field)

        self.assertGreater(os.path.getmtime(copy), 0)

    def test_the_tag_names_each_copy_and_the_sizes(self):
        html = srcset(self._portrait(600), '50vw', 'data-srcset')

        self.assertEqual(html, 'data-srcset="/public/media/sizes/teachers/a-320w.webp 320w, '
                               '/public/media/sizes/teachers/a-480w.webp 480w, '
                               '/public/media/sizes/teachers/a-600w.webp 600w" sizes="50vw"')

    def test_a_missing_or_broken_file_leaves_the_plain_src(self):
        self.assertEqual(srcset(Teacher(profile_image='teachers/gone.jpg').profile_image, '50vw'), '')

        broken = os.path.join(self.media, 'teachers/broken.jpg')
        os.makedirs(os.path.dirname(broken), exist_ok=True)
        with open(broken, 'wb') as f:
            f.write(b'not a photo')
        self.assertEqual(srcset(Teacher(profile_image='teachers/broken.jpg').profile_image, '50vw'), '')

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
