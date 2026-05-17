from django.test import TestCase
from django.urls import reverse

from .models import SitePageContent


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
