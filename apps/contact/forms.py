from django import forms
from captcha.fields import CaptchaField, CaptchaTextInput

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    # The phone keyboard: no capitals or corrections on the code, and Latin input on the left edge.
    captcha = CaptchaField(
        label='کد امنیتی',
        error_messages={'invalid': 'کد امنیتی وارد شده صحیح نیست.'},
        widget=CaptchaTextInput(attrs={'autocapitalize': 'none', 'autocorrect': 'off', 'spellcheck': 'false', 'dir': 'ltr'}),
    )

    class Meta:
        model = ContactMessage
        fields = ('full_name', 'email', 'phone', 'subject', 'message')
        labels = {'phone': 'شماره تماس (اختیاری)'}
        # The model's help texts are written for staff in the admin; the public form has its own hints.
        help_texts = {field: '' for field in fields}
        widgets = {
            'full_name': forms.TextInput(attrs={'autocomplete': 'name'}),
            'email': forms.EmailInput(attrs={
                'placeholder': 'example@email.com',
                'autocomplete': 'email',
                'autocapitalize': 'none',
                'spellcheck': 'false',
                'dir': 'ltr',
            }),
            'phone': forms.TextInput(attrs={'autocomplete': 'tel', 'inputmode': 'tel', 'dir': 'ltr'}),
            'subject': forms.TextInput(),
            'message': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'پیام خود را بنویسید',
            }),
        }
        error_messages = {
            'full_name': {'required': 'لطفا نام و نام خانوادگی را وارد کنید.'},
            'email': {
                'required': 'لطفا ایمیل را وارد کنید.',
                'invalid': 'ایمیل وارد شده معتبر نیست.',
            },
            'subject': {'required': 'لطفا موضوع پیام را وارد کنید.'},
            'message': {'required': 'لطفا متن پیام را وارد کنید.'},
        }

    def full_clean(self):
        super().full_clean()
        # Django links errors to single inputs itself, but not to a multi-part widget like the captcha.
        if 'captcha' in self._errors:
            self.fields['captcha'].widget.attrs['aria-describedby'] = f'{self["captcha"].auto_id}_error'
