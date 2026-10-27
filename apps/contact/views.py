import logging

from django.conf import settings
from django.core.mail import EmailMessage
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .forms import ContactForm

logger = logging.getLogger(__name__)


class ContactView(FormView):
    template_name = 'contact/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact:contact_success')

    def form_valid(self, form):
        message = form.save()
        self.send_notification(message)
        return super().form_valid(form)

    def send_notification(self, message):
        subject = f'پیام جدید از سایت: {message.subject or message.full_name}'
        body = (
            f'نام: {message.full_name}\n'
            f'تلفن: {message.phone}\n'
            f'ایمیل: {message.email or "—"}\n'
            f'موضوع: {message.subject or "—"}\n\n'
            f'{message.message}'
        )
        try:
            EmailMessage(
                subject=subject,
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.CONTACT_NOTIFICATION_EMAIL],
                reply_to=[message.email] if message.email else None,
            ).send(fail_silently=False)
        except Exception:
            # A mail failure must never block the visitor's submission — it's already saved.
            logger.exception('Failed to send contact notification email for message #%s', message.pk)


class ContactSuccessView(TemplateView):
    template_name = 'contact/contact_success.html'
