from django.db import models


class SitePageContent(models.Model):
    HOME = 'home'
    ABOUT = 'about'
    SCHEDULE = 'schedule'
    PAGE_CHOICES = (
        (HOME, 'خانه'),
        (ABOUT, 'درباره ما'),
        (SCHEDULE, 'برنامه کلاس‌ها'),
    )

    page_key = models.CharField('کلید صفحه', max_length=20, choices=PAGE_CHOICES, unique=True, help_text='مشخص می‌کند این محتوا مربوط به کدام صفحه است.')
    title = models.CharField('عنوان', max_length=150, help_text='عنوان اصلی صفحه.')
    body = models.TextField('متن صفحه', help_text='متن اصلی که در صفحه نمایش داده می‌شود.')
    is_active = models.BooleanField('فعال', default=True, help_text='فقط محتوای فعال در صفحه عمومی استفاده می‌شود.')
    created_at = models.DateTimeField('تاریخ ایجاد', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروزرسانی', auto_now=True)

    class Meta:
        ordering = ['page_key']
        verbose_name = 'محتوای صفحه'
        verbose_name_plural = 'محتواهای صفحه'

    def __str__(self):
        return self.get_page_key_display()

# Create your models here.
