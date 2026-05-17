from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    error_messages = {
        'full_name': {'required': 'لطفا نام و نام خانوادگی را وارد کنید.'},
        'email': {
            'required': 'لطفا ایمیل را وارد کنید.',
            'invalid': 'ایمیل وارد شده معتبر نیست.',
        },
        'subject': {'required': 'لطفا موضوع پیام را وارد کنید.'},
        'message': {'required': 'لطفا متن پیام را وارد کنید.'},
    }

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field_errors in self.error_messages.items():
            self.fields[field_name].error_messages.update(field_errors)
