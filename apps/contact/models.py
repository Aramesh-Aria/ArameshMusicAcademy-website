from django.db import models


class ContactMessage(models.Model):
    full_name = models.CharField('نام و نام خانوادگی', max_length=150, help_text='نام فرستنده پیام.')
    email = models.EmailField(
        'ایمیل',
        help_text='آدرس ایمیلی که پاسخ به آن ارسال می‌شود.',
        error_messages={'invalid': 'ایمیل وارد شده معتبر نیست.'},
    )
    phone = models.CharField('شماره تماس', max_length=30, blank=True, help_text='در صورت نیاز شماره تماس را وارد کنید.')
    subject = models.CharField('موضوع', max_length=150, help_text='موضوع اصلی پیام.')
    message = models.TextField('متن پیام', help_text='متن کامل پیام ارسالی.')
    created_at = models.DateTimeField('تاریخ ارسال', auto_now_add=True)
    is_read = models.BooleanField('خوانده شده', default=False, help_text='برای پیگیری، وضعیت خوانده شدن پیام را مشخص کنید.')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'پیام تماس'
        verbose_name_plural = 'پیام‌های تماس'

    def __str__(self):
        return f'{self.full_name} - {self.subject}'

# Create your models here.
