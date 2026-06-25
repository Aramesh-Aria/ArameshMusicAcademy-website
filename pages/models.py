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
    meta_description = models.CharField(
        'توضیحات متا (سئو)',
        max_length=160,
        blank=True,
        help_text='توضیح کوتاه برای موتورهای جستجو و اشتراک‌گذاری (حداکثر ۱۶۰ کاراکتر).',
    )
    hero_image = models.ImageField(
        'تصویر اصلی صفحه',
        upload_to='pages/',
        blank=True,
        help_text='تصویر بزرگ بالای صفحه. در حال حاضر فقط برای صفحه خانه استفاده می‌شود.',
    )
    is_active = models.BooleanField('فعال', default=True, help_text='فقط محتوای فعال در صفحه عمومی استفاده می‌شود.')
    created_at = models.DateTimeField('تاریخ ایجاد', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروزرسانی', auto_now=True)

    class Meta:
        ordering = ['page_key']
        verbose_name = 'محتوای صفحه'
        verbose_name_plural = 'محتواهای صفحه'

    def __str__(self):
        return self.get_page_key_display()

    def save(self, *args, **kwargs):
        try:
            old = SitePageContent.objects.get(pk=self.pk)
            old_hero = old.hero_image.name if old.hero_image else None
        except SitePageContent.DoesNotExist:
            old_hero = None

        new_hero = self.hero_image.name if self.hero_image else None
        hero_changed = old_hero != new_hero

        super().save(*args, **kwargs)

        if hero_changed and self.hero_image:
            from core.image_utils import process_image
            result_name = process_image(self.hero_image, width=1200, height=800, crop=True)
            if result_name != self.hero_image.name:
                SitePageContent.objects.filter(pk=self.pk).update(hero_image=result_name)
                self.hero_image.name = result_name

# Create your models here.
