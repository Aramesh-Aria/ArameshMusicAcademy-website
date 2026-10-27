from django.db import models


class ContactMessage(models.Model):
    full_name = models.CharField('نام و نام خانوادگی', max_length=150, help_text='نام فرستنده پیام.')
    email = models.EmailField(
        'ایمیل',
        blank=True,
        help_text='اختیاری. اگر بازدیدکننده نوشته باشد، پاسخ ایمیلی به آن ارسال می‌شود.',
        error_messages={'invalid': 'ایمیل وارد شده معتبر نیست.'},
    )
    phone = models.CharField('شماره تماس', max_length=30, help_text='شماره‌ای که آموزشگاه برای پاسخ با آن تماس می‌گیرد.')
    subject = models.CharField('موضوع', max_length=150, blank=True, help_text='اختیاری. موضوع اصلی پیام، اگر بازدیدکننده نوشته باشد.')
    message = models.TextField('متن پیام', help_text='متن کامل پیام ارسالی.')
    created_at = models.DateTimeField('تاریخ ارسال', auto_now_add=True)
    is_read = models.BooleanField('خوانده شده', default=False, help_text='برای پیگیری، وضعیت خوانده شدن پیام را مشخص کنید.')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'پیام تماس'
        verbose_name_plural = 'پیام‌های تماس'

    def __str__(self):
        return f'{self.full_name} - {self.subject}' if self.subject else self.full_name

