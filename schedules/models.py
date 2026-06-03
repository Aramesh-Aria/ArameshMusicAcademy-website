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
    name = models.CharField(
        'نام کلاس',
        max_length=120,
        unique=True,
        help_text='برای هر کلاس یک نام یکتا وارد کنید.',
        error_messages={
            'unique': 'کلاسی با این نام قبلا ثبت شده است.',
        },
    )
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
        help_text='کلاسی که این جلسه به آن تعلق دارد.',
    )
    teacher = models.ForeignKey(
        'teachers.Teacher',
        on_delete=models.PROTECT,
        related_name='class_sessions',
        verbose_name='استاد',
        help_text='استادی که این جلسه را برگزار می‌کند.',
    )
    weekday = models.CharField('روز هفته', max_length=3, choices=Weekday.choices, help_text='روز برگزاری این جلسه را انتخاب کنید.')
    weekday_order = models.PositiveSmallIntegerField('ترتیب روز هفته', default=0, editable=False)
    start_time = models.TimeField('ساعت شروع', help_text='ساعت آغاز جلسه.')
    end_time = models.TimeField('ساعت پایان', help_text='ساعت پایان جلسه.')
    is_active = models.BooleanField('فعال', default=True, help_text='فقط جلسه‌های فعال در برنامه سایت نمایش داده می‌شوند.')
    notes = models.TextField('توضیحات', blank=True, help_text='در صورت نیاز توضیح کوتاه درباره این جلسه بنویسید.')
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
                'end_time': 'ساعت پایان باید بعد از ساعت شروع باشد.',
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

        # if self.is_active and overlapping_sessions.exists():
        #     raise ValidationError(
        #         'این استاد در همین روز و بازه زمانی، یک جلسه فعال دیگر دارد.'
        #     )

    def save(self, *args, **kwargs):
        self.weekday_order = WEEKDAY_SORT_VALUES[self.weekday]
        super().save(*args, **kwargs)

# Create your models here.
