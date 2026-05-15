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

WEEKDAY_SORT_VALUES = {
    weekday.value: index
    for index, weekday in enumerate(WEEKDAY_ORDER)
}


class Course(models.Model):
    name = models.CharField('نام کلاس', max_length=120, unique=True)
    created_at = models.DateTimeField('تاریخ ایجاد', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروزرسانی', auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'کلاس'
        verbose_name_plural = 'کلاس‌ها'

    def __str__(self):
        return self.name


class ClassSession(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name='class_sessions',
        verbose_name='کلاس',
    )
    teacher = models.ForeignKey(
        'teachers.Teacher',
        on_delete=models.PROTECT,
        related_name='class_sessions',
        verbose_name='استاد',
    )
    weekday = models.CharField('روز هفته', max_length=3, choices=Weekday.choices)
    weekday_order = models.PositiveSmallIntegerField('ترتیب روز هفته', default=0, editable=False)
    start_time = models.TimeField('ساعت شروع')
    end_time = models.TimeField('ساعت پایان')
    capacity = models.PositiveIntegerField('ظرفیت', null=True, blank=True)
    is_active = models.BooleanField('فعال', default=True)
    notes = models.TextField('توضیحات', blank=True)
    created_at = models.DateTimeField('تاریخ ایجاد', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروزرسانی', auto_now=True)

    class Meta:
        ordering = ['weekday_order', 'start_time', 'teacher__last_name']
        verbose_name = 'جلسه کلاس'
        verbose_name_plural = 'جلسه‌های کلاس'

    def __str__(self):
        return f'{self.course} with {self.teacher} - {self.get_weekday_display()} {self.start_time:%H:%M}'

    def clean(self):
        super().clean()
        if self.start_time and self.end_time and self.end_time <= self.start_time:
            raise ValidationError({
                'end_time': 'End time must be after start time.',
            })
        if self.capacity is not None and self.capacity < 1:
            raise ValidationError({
                'capacity': 'Capacity must be at least 1.',
            })
        if not all([self.teacher_id, self.weekday, self.start_time, self.end_time]):
            return

        overlapping_sessions = ClassSession.objects.filter(
            teacher=self.teacher,
            weekday=self.weekday,
            is_active=True,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        )
        if self.pk:
            overlapping_sessions = overlapping_sessions.exclude(pk=self.pk)

        if self.is_active and overlapping_sessions.exists():
            raise ValidationError(
                'This teacher already has an active class session that overlaps this time.'
            )

    def save(self, *args, **kwargs):
        self.weekday_order = WEEKDAY_SORT_VALUES[self.weekday]
        super().save(*args, **kwargs)

# Create your models here.
