from django.contrib import admin

from .models import ClassSession, Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(ClassSession)
class ClassSessionAdmin(admin.ModelAdmin):
    list_display = (
        'course',
        'teacher',
        'weekday',
        'start_time',
        'end_time',
        'capacity',
        'is_active',
        'updated_at',
    )
    list_filter = ('is_active', 'weekday', 'course', 'teacher')
    search_fields = (
        'course__name',
        'teacher__first_name',
        'teacher__last_name',
        'notes',
    )
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('weekday', 'start_time')

# Register your models here.
