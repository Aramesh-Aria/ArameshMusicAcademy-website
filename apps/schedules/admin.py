from django import forms
from django.contrib import admin

from .models import ClassSession


class ClassSessionForm(forms.ModelForm):
    class Meta:
        model = ClassSession
        fields = '__all__'

    def clean(self):
        # Here rather than in ClassSession.clean(), which cannot see the M2M values.
        cleaned_data = super().clean()
        instruments = cleaned_data.get('instruments')
        programme = cleaned_data.get('programme')
        if programme and instruments:
            raise forms.ValidationError(
                'جلسهٔ رزروشده برای یک دوره ساز دیگری ندارد: یا سازها را انتخاب کنید یا دورهٔ رزروشده را، نه هر دو.'
            )
        if not programme and not instruments:
            self.add_error('instruments', 'حداقل یک ساز، یا یک دورهٔ رزروشده، برای این جلسه انتخاب کنید.')
        return cleaned_data


@admin.register(ClassSession)
class ClassSessionAdmin(admin.ModelAdmin):
    form = ClassSessionForm
    list_display = (
        'teacher',
        'display_offerings',
        'weekday',
        'start_time',
        'end_time',
        'is_active',
        'updated_at',
    )
    list_filter = ('is_active', 'weekday', 'instruments', 'programme', 'teacher')
    search_fields = (
        'teacher__first_name',
        'teacher__last_name',
        'instruments__name',
        'notes',
    )
    filter_horizontal = ('instruments',)
    readonly_fields = ('weekday_order', 'created_at', 'updated_at')
    ordering = ('weekday_order', 'start_time')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('teacher', 'programme').prefetch_related(
            'instruments', 'teacher__programmes',
        )

    @admin.display(description='سازها و دوره‌ها')
    def display_offerings(self, obj):
        return str(obj.offerings())
