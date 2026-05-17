from django.db import models


class SitePageContent(models.Model):
    HOME = 'home'
    ABOUT = 'about'
    PAGE_CHOICES = (
        (HOME, 'خانه'),
        (ABOUT, 'درباره ما'),
    )

    page_key = models.CharField('کلید صفحه', max_length=20, choices=PAGE_CHOICES, unique=True)
    title = models.CharField('عنوان', max_length=150)
    body = models.TextField('متن صفحه')
    is_active = models.BooleanField('فعال', default=True)
    created_at = models.DateTimeField('تاریخ ایجاد', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروزرسانی', auto_now=True)

    class Meta:
        ordering = ['page_key']
        verbose_name = 'محتوای صفحه'
        verbose_name_plural = 'محتواهای صفحه'

    def __str__(self):
        return self.get_page_key_display()

# Create your models here.
