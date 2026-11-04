from django.contrib import admin

from .models import FAQ, Announcement, SitePageContent


@admin.register(SitePageContent)
class SitePageContentAdmin(admin.ModelAdmin):
    list_display = ('page_key', 'title', 'is_active', 'updated_at')
    list_filter = ('page_key', 'is_active')
    search_fields = ('title', 'body')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('page_key',)
    fieldsets = (
        ('صفحه', {
            'fields': ('page_key', 'title', 'body')
        }),
        ('سئو و تصویر', {
            'fields': ('meta_description', 'hero_image')
        }),
        ('انتشار', {
            'fields': ('is_active',)
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'show_on_home', 'is_active', 'display_order', 'updated_at')
    list_filter = ('show_on_home', 'is_active', 'programmes')
    list_editable = ('display_order',)
    search_fields = ('question', 'answer')
    filter_horizontal = ('programmes',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('پرسش', {
            'fields': ('question', 'answer')
        }),
        ('محل نمایش', {
            'fields': ('show_on_home', 'programmes')
        }),
        ('انتشار', {
            'fields': ('is_active', 'display_order')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_active', 'ends_at', 'updated_at')
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    search_fields = ('text',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('اطلاعیه', {
            'fields': ('text',)
        }),
        ('انتشار', {
            'fields': ('is_active', 'ends_at')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at')
        }),
    )
