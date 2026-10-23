from django.db import models


class Testimonial(models.Model):
    author_name = models.CharField(
        'نام',
        max_length=120,
        help_text='نام والد یا هنرجویی که این نظر را گفته است.',
    )
    relation = models.CharField(
        'نسبت',
        max_length=120,
        blank=True,
        help_text='برای مثال: والد هنرجوی پیانو (اختیاری).',
    )
    quote = models.TextField('متن نظر', help_text='متن کوتاه نظر یا تجربه.')
    is_active = models.BooleanField('فعال', default=True, help_text='فقط نظرهای فعال در سایت نمایش داده می‌شوند.')
    display_order = models.PositiveIntegerField('ترتیب نمایش', default=0, help_text='عدد کمتر یعنی نمایش زودتر.')
    created_at = models.DateTimeField('تاریخ ایجاد', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروزرسانی', auto_now=True)

    class Meta:
        ordering = ['display_order', '-created_at']
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرها'

    def __str__(self):
        return self.author_name
