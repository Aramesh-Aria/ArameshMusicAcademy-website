from django.test import TestCase
from django.urls import reverse

from .templatetags.site_tags import fa_digits, local_phone, tel_href


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


class BaseLayoutTests(TestCase):
    def test_every_page_offers_the_primary_phone_and_the_gallery_menu(self):
        response = self.client.get(reverse('contact:contact'))

        self.assertContains(response, 'href="tel:+982144457748"')
        self.assertContains(response, '021 4445 7748')
        self.assertContains(response, 'href="%s"' % reverse('gallery:gallery_root'))

    def test_the_current_section_is_marked_in_the_navigation(self):
        response = self.client.get(reverse('contact:contact'))

        self.assertContains(response, 'aria-current="page"', count=2)  # header and menu


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
