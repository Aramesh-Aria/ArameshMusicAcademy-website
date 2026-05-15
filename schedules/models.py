from django.core.exceptions import ValidationError
from django.db import models


class Weekday(models.TextChoices):
    SATURDAY = 'sat', 'شنبه'
    SUNDAY = 'sun', 'یکشنبه'
    MONDAY = 'mon', 'دوشنبه'
    TUESDAY = 'tue', 'سه‌شنبه'
    WEDNESDAY = 'wed', 'چهارشنبه'
    THURSDAY = 'thu', 'پنجشنبه'
    FRIDAY = 'fri', 'جمعه'


WEEKDAY_ORDER = [
    Weekday.SATURDAY,
    Weekday.SUNDAY,
    Weekday.MONDAY,
    Weekday.TUESDAY,
    Weekday.WEDNESDAY,
    Weekday.THURSDAY,
    Weekday.FRIDAY,
]


class Course(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ClassSession(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name='class_sessions',
    )
    teacher = models.ForeignKey(
        'teachers.Teacher',
        on_delete=models.PROTECT,
        related_name='class_sessions',
    )
    weekday = models.CharField(max_length=3, choices=Weekday.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    capacity = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['weekday', 'start_time', 'teacher__last_name']

    def __str__(self):
        return f'{self.course} with {self.teacher} - {self.get_weekday_display()} {self.start_time:%H:%M}'

    def clean(self):
        super().clean()
        if self.start_time and self.end_time and self.end_time <= self.start_time:
            raise ValidationError({
                'end_time': 'End time must be after start time.',
            })

# Create your models here.
