from django import forms
from captcha.fields import CaptchaField

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    captcha = CaptchaField(label='کد امنیتی', error_messages={'invalid': 'کد امنیتی وارد شده صحیح نیست.'})
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
            'full_name': forms.TextInput(attrs={'autocomplete': 'name'}),
            'email': forms.EmailInput(attrs={
                'placeholder': 'example@email.com',
                'autocomplete': 'email',
            }),
            'phone': forms.TextInput(attrs={'autocomplete': 'tel'}),
            'subject': forms.TextInput(),
            'message': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'پیام خود را بنویسید',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field_errors in self.error_messages.items():
            if field_name in self.fields:
                self.fields[field_name].error_messages.update(field_errors)
        for field in self.fields.values():
            # The model's help texts are written for staff in the admin; the public form has its own hints.
            field.help_text = ''
        self.fields['phone'].label = 'شماره تماس (اختیاری)'
        self.fields['phone'].widget.attrs.update({'inputmode': 'tel', 'dir': 'ltr'})
        self.fields['email'].widget.attrs.update({'dir': 'ltr', 'autocapitalize': 'none', 'spellcheck': 'false'})
        # The phone keyboard: no capitals or corrections on the code, and Latin input on the left edge.
        self.fields['captcha'].widget.attrs.update({'autocapitalize': 'none', 'autocorrect': 'off', 'spellcheck': 'false', 'dir': 'ltr'})


    def full_clean(self):
        super().full_clean()
        # Django links errors to single inputs itself, but not to a multi-part widget like the captcha.
        if 'captcha' in self._errors:
            self.fields['captcha'].widget.attrs['aria-describedby'] = f'{self["captcha"].auto_id}_error'
