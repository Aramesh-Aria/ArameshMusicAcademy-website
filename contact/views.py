from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .forms import ContactForm


class ContactView(FormView):
    template_name = 'contact/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact:contact_success')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ContactSuccessView(TemplateView):
    template_name = 'contact/contact_success.html'

# Create your views here.
