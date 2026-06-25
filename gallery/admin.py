from django.contrib import admin
from django.utils.html import format_html

from .models import GalleryImage, GalleryPage, Video


class VideoInline(admin.TabularInline):
    model = Video
    extra = 1
    fields = ('title', 'platform', 'video_url', 'caption', 'is_active', 'display_order')


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1
    fields = (
        'image_preview',
        'image',
        'title',
        'caption',
        'is_active',
        'display_order',
    )
    readonly_fields = ('image_preview',)

    @admin.display(description='پیش‌نمایش')
    def image_preview(self, obj):
        if not obj.image:
            return 'بدون تصویر'
        return format_html(
            '<img src="{}" style="width: 80px; height: 60px; object-fit: cover;" />',
            obj.image.url,
        )


@admin.register(GalleryPage)
class GalleryPageAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'parent',
        'slug',
        'slug_path_display',
        'is_active',
        'display_order',
        'updated_at',
    )
    list_filter = ('is_active', 'parent')
    search_fields = ('title', 'slug', 'description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('cover_image_preview', 'slug_path_display', 'created_at', 'updated_at')
    ordering = ('parent__title', 'display_order', 'title')
    inlines = (GalleryImageInline, VideoInline)
    fieldsets = (
        ('اطلاعات صفحه', {
            'fields': ('title', 'slug', 'parent', 'description', 'intro_text', 'cover_image', 'cover_image_preview')
        }),
        ('انتشار', {
            'fields': ('is_active', 'display_order')
        }),
        ('آدرس و تاریخ‌ها', {
            'fields': ('slug_path_display', 'created_at', 'updated_at')
        }),
    )

    @admin.display(description='مسیر کامل')
    def slug_path_display(self, obj):
        if not obj.pk:
            return 'بعد از ذخیره ساخته می‌شود.'
        return obj.slug_path

    @admin.display(description='پیش‌نمایش کاور')
    def cover_image_preview(self, obj):
        if not obj.cover_image:
            return 'بدون تصویر'
        return format_html(
            '<img src="{}" style="width: 120px; height: 80px; object-fit: cover;" />',
            obj.cover_image.url,
        )


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = (
        'image_preview',
        'title',
        'gallery_page',
        'is_active',
        'display_order',
        'updated_at',
    )
    list_filter = ('is_active', 'gallery_page')
    search_fields = ('title', 'caption', 'gallery_page__title')
    readonly_fields = ('image_preview', 'created_at', 'updated_at')
    ordering = ('gallery_page', 'display_order', 'created_at')

    @admin.display(description='پیش‌نمایش')
    def image_preview(self, obj):
        if not obj.image:
            return 'بدون تصویر'
        return format_html(
            '<img src="{}" style="width: 80px; height: 60px; object-fit: cover;" />',
            obj.image.url,
        )


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'platform', 'gallery_page', 'is_active', 'display_order', 'updated_at')
    list_filter = ('is_active', 'platform', 'gallery_page')
    search_fields = ('title', 'caption', 'gallery_page__title')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('gallery_page', 'display_order', 'created_at')
