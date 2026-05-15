from django.contrib import admin
from django.utils.html import format_html
from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin  # noqa: F401

from .models import Instrument, Teacher


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        'profile_image_preview',
        'full_name',
        'instrument_list',
        'birth_place',
        'birth_city',
        'is_active',
        'display_order',
        'updated_at',
    )
    list_filter = (
        'is_active',
        'instruments',
        'birth_province',
        'birth_city',
        ('date_of_birth', JDateFieldListFilter),
    )
    search_fields = ('first_name', 'last_name', 'education', 'biography')
    filter_horizontal = ('instruments',)
    readonly_fields = ('profile_image_preview', 'created_at', 'updated_at')
    ordering = ('display_order', 'last_name', 'first_name')
    fieldsets = (
        ('اطلاعات شخصی', {
            'fields': (
                'first_name',
                'last_name',
                'date_of_birth',
                'birth_province',
                'birth_city',
                'profile_image',
                'profile_image_preview',
            )
        }),
        ('پروفایل آموزشی', {
            'fields': ('instruments', 'education', 'biography')
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

    @admin.display(description='محل تولد')
    def birth_place(self, obj):
        return f'{obj.birth_province}، {obj.birth_city}'

    @admin.display(description='تصویر')
    def profile_image_preview(self, obj):
        if not obj.profile_image:
            return 'بدون تصویر'
        return format_html(
            '<img src="{}" style="width: 56px; height: 56px; object-fit: cover; border-radius: 6px;" />',
            obj.profile_image.url,
        )

# Register your models here.
