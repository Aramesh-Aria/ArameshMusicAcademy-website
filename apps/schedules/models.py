from dataclasses import dataclass

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


@dataclass(frozen=True)
class Offerings:
    """A session's Instruments and Programmes, in the order the schedule lists them."""
    instruments: list
    programmes: list

    @classmethod
    def combine(cls, sessions):
        """Everything `sessions` offer between them, each named once, in display order."""
        instruments, programmes = {}, {}
        for session in sessions:
            offerings = session.offerings()
            instruments.update((i.pk, i) for i in offerings.instruments)
            programmes.update((p.pk, p) for p in offerings.programmes)
        in_order = lambda items: sorted(items.values(), key=lambda item: (item.display_order, item.name))
        return cls(instruments=in_order(instruments), programmes=in_order(programmes))

    @property
    def names(self):
        return [item.name for item in self.instruments + self.programmes]

    def __str__(self):
        # «پیانو، گیتار پاپ؛ تئوری و سلفژ»: a Persian semicolon, since a middle dot reads like the digit zero (۰).
        parts = ['، '.join(item.name for item in group) for group in (self.instruments, self.programmes) if group]
        return '؛ '.join(parts)


class ClassSessionQuerySet(models.QuerySet):
    def active(self):
        """The sessions the site shows: active, and taught by an active teacher."""
        return self.filter(is_active=True, teacher__is_active=True)


class ClassSession(models.Model):
    teacher = models.ForeignKey(
        'teachers.Teacher',
        on_delete=models.PROTECT,
        related_name='class_sessions',
        verbose_name='استاد',
        help_text='استادی که این جلسه را برگزار می‌کند.',
    )
    instruments = models.ManyToManyField(
        'teachers.Instrument',
        related_name='class_sessions',
        verbose_name='سازها',
        blank=True,
        help_text='یک یا چند سازی که استاد در این جلسه تدریس می‌کند را انتخاب کنید.',
    )
    programme = models.ForeignKey(
        'programmes.Programme',
        on_delete=models.PROTECT,
        related_name='reserved_sessions',
        null=True,
        blank=True,
        limit_choices_to={'kind': 'fixed_time'},
        verbose_name='دورهٔ رزروشده',
        help_text='فقط برای جلسه‌ای که برای یک دورهٔ زمان‌دار (مثل گروه نوازی) رزرو شده است. '
                  'در این جلسه چیز دیگری تدریس نمی‌شود.',
    )
    weekday = models.CharField('روز هفته', max_length=3, choices=Weekday.choices, help_text='روز برگزاری این جلسه را انتخاب کنید.')
    weekday_order = models.PositiveSmallIntegerField('ترتیب روز هفته', default=0, editable=False)
    start_time = models.TimeField('ساعت شروع', help_text='ساعت آغاز جلسه.')
    end_time = models.TimeField('ساعت پایان', help_text='ساعت پایان جلسه.')
    is_active = models.BooleanField('فعال', default=True, help_text='فقط جلسه‌های فعال در برنامه سایت نمایش داده می‌شوند.')
    notes = models.TextField('توضیحات', blank=True, help_text='در صورت نیاز توضیح کوتاه درباره این جلسه بنویسید.')
    created_at = models.DateTimeField('تاریخ ایجاد', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروزرسانی', auto_now=True)

    objects = ClassSessionQuerySet.as_manager()

    class Meta:
        ordering = ['weekday_order', 'start_time', 'teacher__last_name']
        verbose_name = 'جلسه کلاس'
        verbose_name_plural = 'جلسه‌های کلاس'

    def __str__(self):
        return f'{self.teacher} - {self.get_weekday_display()} {self.start_time:%H:%M}'

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

        if self.is_active and overlapping_sessions.exists():
            raise ValidationError(
                'این استاد در همین روز و بازه زمانی، یک جلسه فعال دیگر دارد.'
            )

    def offerings(self):
        """What the schedule shows for this session (ADR-0002).

        A session reserved for a fixed-time Programme shows only that Programme. Any other shows its
        Instruments (children-only ones excluded), then the teacher's "with the teacher" Programmes.
        Reads `instruments` and `teacher.programmes` through `.all()`, so a prefetch serves it.
        """
        if self.programme_id:
            return Offerings(instruments=[], programmes=[self.programme])
        return Offerings(
            instruments=[i for i in self.instruments.all() if not i.children_only],
            programmes=[
                p for p in self.teacher.programmes.all()
                if p.is_active and p.kind == p.Kind.WITH_TEACHER
            ],
        )

    def save(self, *args, **kwargs):
        self.weekday_order = WEEKDAY_SORT_VALUES[self.weekday]
        super().save(*args, **kwargs)

# Create your models here.
