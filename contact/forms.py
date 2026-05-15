from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ('full_name', 'email', 'phone', 'subject', 'message')
        widgets = {
            'full_name': forms.TextInput(attrs={
                'placeholder': 'نام و نام خانوادگی',
                'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'example@email.com',
                'autocomplete': 'email',
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'شماره تماس',
                'autocomplete': 'tel',
            }),
            'subject': forms.TextInput(attrs={
                'placeholder': 'موضوع پیام',
            }),
            'message': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'پیام خود را بنویسید',
            }),
        }
