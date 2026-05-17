from django.contrib import admin

from .models import SitePageContent


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
        ('انتشار', {
            'fields': ('is_active',)
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at')
        }),
    )

# Register your models here.
