from django.contrib import admin

from .models import Programme


@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):
    list_display = ('name', 'kind', 'age_label', 'is_active', 'display_order', 'updated_at')
    list_filter = ('kind', 'is_active')
    search_fields = ('name', 'short_description', 'long_description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('display_order', 'name')
    fieldsets = (
        ('دوره', {
            'fields': ('name', 'slug', 'kind', 'age_label')
        }),
        ('متن', {
            'fields': ('short_description', 'long_description')
        }),
        ('تصاویر و سازها', {
            'fields': ('photo_1', 'photo_2', 'photo_3', 'instruments_shown')
        }),
        ('انتشار', {
            'fields': ('is_active', 'display_order')
        }),
        ('تاریخ‌های سیستمی', {
            'fields': ('created_at', 'updated_at')
        }),
    )
