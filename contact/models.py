from django.db import models


class ContactMessage(models.Model):
    full_name = models.CharField('نام و نام خانوادگی', max_length=150)
    email = models.EmailField('ایمیل')
    phone = models.CharField('شماره تماس', max_length=30, blank=True)
    subject = models.CharField('موضوع', max_length=150)
    message = models.TextField('متن پیام')
    created_at = models.DateTimeField('تاریخ ارسال', auto_now_add=True)
    is_read = models.BooleanField('خوانده شده', default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'پیام تماس'
        verbose_name_plural = 'پیام‌های تماس'

    def __str__(self):
        return f'{self.full_name} - {self.subject}'

# Create your models here.
