from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class GalleryPage(models.Model):
    title = models.CharField('عنوان', max_length=150, help_text='نامی که در لیست گالری و صفحه نمایش داده می‌شود.')
    slug = models.SlugField(
        'نام در آدرس',
        max_length=150,
        blank=True,
        help_text='اگر خالی بماند، به صورت خودکار از عنوان ساخته می‌شود.',
        error_messages={
            'invalid': 'نام در آدرس فقط می‌تواند شامل حروف، عدد، خط فاصله و زیرخط باشد.',
        },
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        verbose_name='گالری والد',
        null=True,
        blank=True,
        help_text='برای ساخت زیرگالری، صفحه والد را انتخاب کنید.',
    )
    description = models.TextField('توضیحات', blank=True, help_text='توضیح کوتاه مدیریتی یا توضیح عمومی صفحه گالری.')
    intro_text = models.TextField('متن معرفی', blank=True, help_text='متنی که بالای تصاویر این گالری در سایت نمایش داده می‌شود.')
    cover_image = models.ImageField('تصویر کاور', upload_to='gallery/covers/', blank=True, help_text='تصویر شاخص این صفحه گالری.')
    is_active = models.BooleanField('فعال', default=True, help_text='فقط گالری‌های فعال در سایت قابل مشاهده هستند.')
    display_order = models.PositiveIntegerField('ترتیب نمایش', default=0, help_text='عدد کمتر یعنی نمایش زودتر در لیست گالری‌ها.')
    created_at = models.DateTimeField('تاریخ ایجاد', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروزرسانی', auto_now=True)

    class Meta:
        ordering = ['display_order', 'title']
        verbose_name = 'صفحه گالری'
        verbose_name_plural = 'صفحه‌های گالری'
        constraints = [
            models.UniqueConstraint(
                fields=['parent', 'slug'],
                name='unique_gallery_page_slug_per_parent',
            ),
        ]

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        if not self.slug and self.title:
            self.slug = slugify(self.title, allow_unicode=True)

        if self.pk is not None and self.parent_id == self.pk:
            raise ValidationError({'parent': 'یک صفحه گالری نمی‌تواند والد خودش باشد.'})

        parent = self.parent
        while parent:
            if parent.pk == self.pk:
                raise ValidationError({'parent': 'یک صفحه گالری نمی‌تواند یکی از فرزندان خودش را به عنوان والد انتخاب کند.'})
            parent = parent.parent

        duplicate_slug_query = GalleryPage.objects.filter(
            parent=self.parent,
            slug=self.slug,
        )
        if self.pk:
            duplicate_slug_query = duplicate_slug_query.exclude(pk=self.pk)
        if self.slug and duplicate_slug_query.exists():
            raise ValidationError({
                'slug': 'این نام در آدرس قبلا در همین سطح از گالری استفاده شده است. نام دیگری انتخاب کنید.',
            })

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    @property
    def slug_path(self):
        slugs = [self.slug]
        parent = self.parent
        while parent:
            slugs.append(parent.slug)
            parent = parent.parent
        return '/'.join(reversed(slugs))

    def get_absolute_url(self):
        return reverse('gallery:gallery_detail', kwargs={'slug_path': self.slug_path})


class GalleryImage(models.Model):
    gallery_page = models.ForeignKey(
        GalleryPage,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='صفحه گالری',
        help_text='تصویر به کدام صفحه گالری تعلق دارد.',
    )
    title = models.CharField('عنوان', max_length=150, blank=True, help_text='در صورت نیاز برای این تصویر عنوان وارد کنید.')
    image = models.ImageField('تصویر', upload_to='gallery/', help_text='فایل تصویر را بارگذاری کنید.')
    caption = models.TextField('توضیح تصویر', blank=True, help_text='متن کوتاه زیر تصویر یا توضیح تکمیلی.')
    is_active = models.BooleanField('فعال', default=True, help_text='فقط تصاویر فعال در سایت نمایش داده می‌شوند.')
    display_order = models.PositiveIntegerField('ترتیب نمایش', default=0, help_text='عدد کمتر یعنی نمایش زودتر در گالری.')
    created_at = models.DateTimeField('تاریخ ایجاد', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروزرسانی', auto_now=True)

    class Meta:
        ordering = ['display_order', 'created_at']
        verbose_name = 'تصویر گالری'
        verbose_name_plural = 'تصاویر گالری'

    def __str__(self):
        if self.title:
            return self.title
        return f'تصویر {self.gallery_page}'
