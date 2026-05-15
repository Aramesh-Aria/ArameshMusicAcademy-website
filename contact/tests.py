from django.test import TestCase
from django.urls import reverse

from .forms import ContactForm
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


class ContactMessageModelTests(TestCase):
    def test_contact_message_string_contains_name_and_subject(self):
        message = ContactMessage(
            full_name='Ali Ahmadi',
            email='ali@example.com',
            subject='Question',
            message='I want more information.',
        )

        self.assertEqual(str(message), 'Ali Ahmadi - Question')


class ContactFormTests(TestCase):
    def test_contact_form_uses_persian_labels_and_widgets(self):
        form = ContactForm()

        self.assertEqual(form.fields['full_name'].label, 'نام و نام خانوادگی')
        self.assertEqual(form.fields['message'].widget.attrs['placeholder'], 'پیام خود را بنویسید')

# Create your tests here.
