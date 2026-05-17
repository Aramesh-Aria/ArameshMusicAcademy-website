from django.contrib import admin

from .models import ClassSession, Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ClassSession)
class ClassSessionAdmin(admin.ModelAdmin):
    list_display = (
        'course',
        'teacher',
        'weekday',
        'weekday_order',
        'start_time',
        'end_time',
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
    readonly_fields = ('weekday_order', 'created_at', 'updated_at')
    ordering = ('weekday_order', 'start_time')

# Register your models here.
