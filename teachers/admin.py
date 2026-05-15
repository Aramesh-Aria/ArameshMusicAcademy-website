from django.contrib import admin
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
        'full_name',
        'instrument_list',
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
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('display_order', 'last_name', 'first_name')
    fieldsets = (
        ('Personal information', {
            'fields': (
                'first_name',
                'last_name',
                'date_of_birth',
                'birth_province',
                'birth_city',
                'profile_image',
            )
        }),
        ('Teaching profile', {
            'fields': ('instruments', 'education', 'biography')
        }),
        ('Publishing', {
            'fields': ('is_active', 'display_order')
        }),
        ('System dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    @admin.display(description='Instruments')
    def instrument_list(self, obj):
        return ', '.join(instrument.name for instrument in obj.instruments.all())

# Register your models here.
