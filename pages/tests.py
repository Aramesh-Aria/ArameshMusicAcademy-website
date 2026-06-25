from django.test import TestCase
from django.urls import reverse

from teachers.models import Teacher
from testimonials.models import Testimonial

from .models import SitePageContent


class HomeContextTests(TestCase):
    def test_home_context_includes_preview_sections(self):
        teacher = Teacher.objects.create(
            first_name='Sara',
            last_name='Karimi',
            biography='Bio',
            profile_image='teachers/sara.jpg',
            is_active=True,
        )
        Testimonial.objects.create(author_name='مادر آرمین', quote='عالی بود.', is_active=True)

        response = self.client.get(reverse('pages:home'))

        self.assertIn(teacher, list(response.context['featured_teachers']))
        self.assertEqual(len(response.context['testimonials']), 1)
        self.assertIn('gallery_preview_images', response.context)
        self.assertTrue(response.context['meta_description'])


class PageViewTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse('pages:home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'آموزشگاه موسیقی آرامش')

    def test_about_page_loads(self):
        response = self.client.get(reverse('pages:about'))

        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_admin_managed_content_when_available(self):
        SitePageContent.objects.create(
            page_key=SitePageContent.HOME,
            title='خانه جدید',
            body='متن صفحه خانه از پنل مدیریت.',
            is_active=True,
        )

        response = self.client.get(reverse('pages:home'))

        self.assertContains(response, 'خانه جدید')
        self.assertContains(response, 'متن صفحه خانه از پنل مدیریت.')

# Create your tests here.
