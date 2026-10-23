from django import forms
from django.contrib import admin

from .models import ClassSession


class ClassSessionForm(forms.ModelForm):
    class Meta:
        model = ClassSession
        fields = '__all__'

    def clean_instruments(self):
        instruments = self.cleaned_data.get('instruments')
        if not instruments:
            raise forms.ValidationError('حداقل یک ساز برای این جلسه انتخاب کنید.')
        return instruments


@admin.register(ClassSession)
class ClassSessionAdmin(admin.ModelAdmin):
    form = ClassSessionForm
    list_display = (
        'teacher',
        'display_instruments',
        'weekday',
        'start_time',
        'end_time',
        'is_active',
        'updated_at',
    )
    list_filter = ('is_active', 'weekday', 'instruments', 'teacher')
    search_fields = (
        'teacher__first_name',
        'teacher__last_name',
        'instruments__name',
        'notes',
    )
    filter_horizontal = ('instruments',)
    readonly_fields = ('weekday_order', 'created_at', 'updated_at')
    ordering = ('weekday_order', 'start_time')

    @admin.display(description='سازها')
    def display_instruments(self, obj):
        return '، '.join(instrument.name for instrument in obj.instruments.all())
