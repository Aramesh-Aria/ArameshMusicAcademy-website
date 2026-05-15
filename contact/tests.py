from django.test import TestCase
from django.urls import reverse

from .models import ContactMessage


class ContactViewTests(TestCase):
    def test_contact_form_saves_message(self):
        response = self.client.post(reverse('contact:contact'), {
            'full_name': 'Ali Ahmadi',
            'email': 'ali@example.com',
            'phone': '09120000000',
            'subject': 'Question',
            'message': 'I want more information.',
        })

        self.assertRedirects(response, reverse('contact:contact_success'))
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(ContactMessage.objects.get().full_name, 'Ali Ahmadi')

# Create your tests here.
