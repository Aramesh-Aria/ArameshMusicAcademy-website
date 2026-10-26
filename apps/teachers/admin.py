from django.contrib import admin
from django.utils.html import format_html

from .models import Instrument, Teacher


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'children_only', 'display_order', 'updated_at')
    list_filter = ('children_only',)
    list_editable = ('display_order',)
    search_fields = ('name', 'overview')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('ساز', {
            'fields': ('name', 'slug', 'children_only')
        }),
        ('صفحهٔ ساز', {
            'fields': ('overview', 'photo')
        }),
        ('انتشار', {
            'fields': ('display_order',)
        }),
        ('تاریخ‌های سیستمی', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        'profile_image_preview',
        'full_name',
        'instrument_list',
        'programme_list',
        'is_active',
        'display_order',
        'updated_at',
    )
    list_filter = (
        'is_active',
        'instruments',
        'programmes',
    )
    search_fields = ('first_name', 'last_name', 'biography')
    filter_horizontal = ('instruments', 'programmes')
    readonly_fields = ('profile_image_preview', 'created_at', 'updated_at')
    ordering = ('display_order', 'last_name', 'first_name')
    fieldsets = (
        ('اطلاعات شخصی', {
            'fields': (
                'first_name',
                'last_name',
                'profile_image',
                'profile_image_preview',
            )
        }),
        ('پروفایل آموزشی', {
            'fields': ('instruments', 'programmes', 'lineage', 'biography', 'home_intro')
        }),
        ('انتشار', {
            'fields': ('is_active', 'display_order')
        }),
        ('تاریخ‌های سیستمی', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    @admin.display(description='سازها')
    def instrument_list(self, obj):
        return ', '.join(instrument.name for instrument in obj.instruments.all())

    @admin.display(description='دوره‌ها')
    def programme_list(self, obj):
        return ', '.join(programme.name for programme in obj.programmes.all())

    @admin.display(description='تصویر')
    def profile_image_preview(self, obj):
        if not obj.profile_image:
            return 'بدون تصویر'
        return format_html(
            '<img src="{}" style="width: 56px; height: 56px; object-fit: cover; border-radius: 6px;" />',
            obj.profile_image.url,
        )

