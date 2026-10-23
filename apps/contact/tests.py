from captcha.models import CaptchaStore
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse

from .forms import ContactForm
from .models import ContactMessage


class AdminUnreadCountTests(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            username='admin', email='admin@example.com', password='pass12345',
        )
        self.client.force_login(self.admin)

    def _make_message(self, is_read):
        ContactMessage.objects.create(
            full_name='Ali', email='a@example.com', subject='Q',
            message='hi', is_read=is_read,
        )

    def test_sidebar_shows_unread_message_count(self):
        self._make_message(is_read=False)
        self._make_message(is_read=False)
        self._make_message(is_read=True)  # read ones must not be counted

        response = self.client.get(reverse('admin:index'))

        self.assertContains(response, 'پیام‌های تماس (2)')

    def test_no_count_when_all_read(self):
        self._make_message(is_read=True)

        response = self.client.get(reverse('admin:index'))

        self.assertNotContains(response, 'پیام‌های تماس (')


class ContactViewTests(TestCase):
    def _solved_captcha(self):
        """Create a real captcha and return its (hashkey, correct response)."""
        key = CaptchaStore.generate_key()
        response = CaptchaStore.objects.get(hashkey=key).response
        return key, response

    def test_contact_form_saves_message_and_sends_notification(self):
        captcha_key, captcha_response = self._solved_captcha()
        response = self.client.post(reverse('contact:contact'), {
            'full_name': 'Ali Ahmadi',
            'email': 'ali@example.com',
            'phone': '09120000000',
            'subject': 'Question',
            'message': 'I want more information.',
            'captcha_0': captcha_key,
            'captcha_1': captcha_response,
        })

        self.assertRedirects(response, reverse('contact:contact_success'))
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(ContactMessage.objects.get().full_name, 'Ali Ahmadi')

        # The academy is notified, with the visitor's address as reply-to.
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('ali@example.com', mail.outbox[0].reply_to)
        self.assertIn('Question', mail.outbox[0].subject)


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

    def test_contact_form_invalid_email_uses_persian_message(self):
        form = ContactForm(data={
            'full_name': 'Ali Ahmadi',
            'email': 'invalid-email',
            'phone': '09120000000',
            'subject': 'Question',
            'message': 'I want more information.',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('ایمیل وارد شده معتبر نیست.', form.errors['email'])

# Create your tests here.
