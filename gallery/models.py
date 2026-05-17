from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class GalleryPage(models.Model):
    title = models.CharField('عنوان', max_length=150)
    slug = models.SlugField('نام در آدرس', max_length=150)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        verbose_name='گالری والد',
        null=True,
        blank=True,
    )
    description = models.TextField('توضیحات', blank=True)
    is_active = models.BooleanField('فعال', default=True)
    display_order = models.PositiveIntegerField('ترتیب نمایش', default=0)
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
        if self.pk is not None and self.parent_id == self.pk:
            raise ValidationError({'parent': 'A gallery page cannot be its own parent.'})

        parent = self.parent
        while parent:
            if parent.pk == self.pk:
                raise ValidationError({'parent': 'A gallery page cannot use one of its children as parent.'})
            parent = parent.parent

        duplicate_slug_query = GalleryPage.objects.filter(
            parent=self.parent,
            slug=self.slug,
        )
        if self.pk:
            duplicate_slug_query = duplicate_slug_query.exclude(pk=self.pk)
        if self.slug and duplicate_slug_query.exists():
            raise ValidationError({
                'slug': 'This address name is already used in this gallery level. Choose a different one.',
            })

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
    )
    title = models.CharField('عنوان', max_length=150, blank=True)
    image = models.ImageField('تصویر', upload_to='gallery/')
    caption = models.TextField('توضیح تصویر', blank=True)
    is_active = models.BooleanField('فعال', default=True)
    display_order = models.PositiveIntegerField('ترتیب نمایش', default=0)
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

# Create your models here.
