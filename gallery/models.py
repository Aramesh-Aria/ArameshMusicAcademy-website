import re
from urllib.parse import parse_qs, urlparse

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def youtube_video_id(url):
    """Extract the 11-char video id from any common YouTube URL form."""
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    if 'youtu.be' in host:
        return parsed.path.lstrip('/').split('/')[0] or None
    if 'youtube' in host:
        if parsed.path.startswith(('/embed/', '/shorts/')):
            return parsed.path.split('/')[2] or None
        query_id = parse_qs(parsed.query).get('v', [None])[0]
        return query_id
    return None


def aparat_video_hash(url):
    """Extract the video hash from an Aparat URL (aparat.com/v/HASH or embed form)."""
    match = re.search(r'/v/([A-Za-z0-9]+)', url) or re.search(r'/videohash/([A-Za-z0-9]+)', url)
    return match.group(1) if match else None


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

        try:
            old = GalleryPage.objects.get(pk=self.pk)
            old_cover = old.cover_image.name if old.cover_image else None
        except GalleryPage.DoesNotExist:
            old_cover = None

        new_cover = self.cover_image.name if self.cover_image else None
        cover_changed = old_cover != new_cover

        super().save(*args, **kwargs)

        if cover_changed and self.cover_image:
            from core.image_utils import process_image
            result_name = process_image(self.cover_image, width=900, height=600, crop=True)
            if result_name != self.cover_image.name:
                GalleryPage.objects.filter(pk=self.pk).update(cover_image=result_name)
                self.cover_image.name = result_name

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

    def save(self, *args, **kwargs):
        try:
            old = GalleryImage.objects.get(pk=self.pk)
            old_name = old.image.name if old.image else None
        except GalleryImage.DoesNotExist:
            old_name = None

        new_name = self.image.name if self.image else None
        image_changed = old_name != new_name

        super().save(*args, **kwargs)

        if image_changed and self.image:
            from core.image_utils import process_image
            result_name = process_image(self.image, width=1920, height=1920, crop=False)
            if result_name != self.image.name:
                GalleryImage.objects.filter(pk=self.pk).update(image=result_name)
                self.image.name = result_name

    def __str__(self):
        if self.title:
            return self.title
        return f'تصویر {self.gallery_page}'


class Video(models.Model):
    YOUTUBE = 'youtube'
    APARAT = 'aparat'
    PLATFORM_CHOICES = (
        (YOUTUBE, 'یوتیوب'),
        (APARAT, 'آپارات'),
    )

    gallery_page = models.ForeignKey(
        GalleryPage,
        on_delete=models.CASCADE,
        related_name='videos',
        verbose_name='صفحه گالری',
        help_text='ویدیو به کدام صفحه گالری تعلق دارد.',
    )
    title = models.CharField('عنوان', max_length=150, help_text='عنوان ویدیو.')
    platform = models.CharField('سرویس', max_length=10, choices=PLATFORM_CHOICES, help_text='ویدیو از کدام سرویس جاسازی می‌شود.')
    video_url = models.URLField(
        'آدرس ویدیو',
        help_text='آدرس صفحه ویدیو در یوتیوب یا آپارات را وارد کنید (نه کد جاسازی).',
    )
    caption = models.TextField('توضیح', blank=True, help_text='توضیح کوتاه زیر ویدیو.')
    is_active = models.BooleanField('فعال', default=True, help_text='فقط ویدیوهای فعال در سایت نمایش داده می‌شوند.')
    display_order = models.PositiveIntegerField('ترتیب نمایش', default=0, help_text='عدد کمتر یعنی نمایش زودتر.')
    created_at = models.DateTimeField('تاریخ ایجاد', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروزرسانی', auto_now=True)

    class Meta:
        ordering = ['display_order', 'created_at']
        verbose_name = 'ویدیو'
        verbose_name_plural = 'ویدیوها'

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        if not self.video_url:
            return
        if self.platform == self.YOUTUBE and not youtube_video_id(self.video_url):
            raise ValidationError({'video_url': 'آدرس یوتیوب معتبر نیست.'})
        if self.platform == self.APARAT and not aparat_video_hash(self.video_url):
            raise ValidationError({'video_url': 'آدرس آپارات معتبر نیست.'})

    @property
    def embed_url(self):
        """The iframe src for embedding this video, or None if it can't be parsed."""
        if self.platform == self.YOUTUBE:
            video_id = youtube_video_id(self.video_url)
            return f'https://www.youtube.com/embed/{video_id}' if video_id else None
        if self.platform == self.APARAT:
            video_hash = aparat_video_hash(self.video_url)
            return f'https://www.aparat.com/video/video/embed/videohash/{video_hash}/vt/frame' if video_hash else None
        return None
