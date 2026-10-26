from django.db import models
from django.db.models import Q
from django.urls import reverse

PHOTO_FIELDS = ('photo_1', 'photo_2', 'photo_3')


class ProgrammeQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class Programme(models.Model):
    """A way of studying at the Academy, independent of any one Instrument (ADR-0002)."""

    class Kind(models.TextChoices):
        WITH_TEACHER = 'with_teacher', 'با استاد (هر زمان که استاد حضور دارد)'
        FIXED_TIME = 'fixed_time', 'زمان ثابت (جلسهٔ رزروشده)'

    class InstrumentsShown(models.TextChoices):
        ALL = 'all', 'همهٔ سازها'
        CHILDREN_ONLY = 'children_only', 'فقط سازهای کودک'
        NONE = 'none', 'هیچ‌کدام'

    name = models.CharField(
        'نام دوره',
        max_length=100,
        unique=True,
        error_messages={'unique': 'دوره‌ای با این نام قبلا ثبت شده است.'},
    )
    slug = models.SlugField(
        'نام در آدرس',
        max_length=100,
        unique=True,
        help_text='با حروف لاتین، مثل theory. در آدرس صفحهٔ دوره می‌آید.',
    )
    kind = models.CharField(
        'نوع دوره',
        max_length=20,
        choices=Kind.choices,
        default=Kind.WITH_TEACHER,
        help_text='«با استاد»: هر روزی که استادِ این دوره در آموزشگاه است. '
                  '«زمان ثابت»: یک جلسهٔ مشخص در برنامه برای این دوره رزرو می‌شود (مثل گروه نوازی).',
    )
    short_description = models.TextField('توضیح کوتاه', help_text='برای کارت دوره، حدود ۲۵ کلمه.')
    long_description = models.TextField('توضیح کامل', help_text='برای صفحهٔ دوره. یک خط خالی بین پاراگراف‌ها بگذارید.')
    age_label = models.CharField(
        'برچسب سن',
        max_length=40,
        blank=True,
        help_text='متن کوتاه روی کارت، مثل «از ۷ سال». اگر خالی بماند نمایش داده نمی‌شود.',
    )
    photo_1 = models.ImageField('تصویر ۱', upload_to='programmes/', blank=True)
    photo_2 = models.ImageField('تصویر ۲', upload_to='programmes/', blank=True)
    photo_3 = models.ImageField(
        'تصویر ۳',
        upload_to='programmes/',
        blank=True,
        help_text='تا سه تصویر که در کارت دوره یکی‌یکی نمایش داده می‌شوند.',
    )
    instruments_shown = models.CharField(
        'سازهای صفحهٔ دوره',
        max_length=20,
        choices=InstrumentsShown.choices,
        default=InstrumentsShown.NONE,
        help_text='کدام سازها در صفحهٔ این دوره فهرست شوند.',
    )
    display_order = models.PositiveIntegerField('ترتیب نمایش', default=0, help_text='عدد کمتر یعنی نمایش زودتر.')
    is_active = models.BooleanField('فعال', default=True, help_text='فقط دوره‌های فعال در سایت نمایش داده می‌شوند.')
    created_at = models.DateTimeField('تاریخ ایجاد', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروزرسانی', auto_now=True)

    objects = ProgrammeQuerySet.as_manager()

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = 'دوره'
        verbose_name_plural = 'دوره‌ها'

    # What a Teacher can be tagged with: "with the teacher" Programmes other than private lessons,
    # which are implied for every Teacher (every lesson at the Academy is private).
    TEACHER_CHOICES = Q(kind=Kind.WITH_TEACHER) & ~Q(instruments_shown=InstrumentsShown.ALL)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('programmes:programme_detail', kwargs={'slug': self.slug})

    @property
    def photos(self):
        return [getattr(self, field) for field in PHOTO_FIELDS if getattr(self, field)]

    def save(self, *args, **kwargs):
        try:
            old = Programme.objects.get(pk=self.pk)
            old_names = {field: getattr(old, field).name for field in PHOTO_FIELDS}
        except Programme.DoesNotExist:
            old_names = {}

        changed = [
            field for field in PHOTO_FIELDS
            if getattr(self, field) and getattr(self, field).name != old_names.get(field)
        ]

        super().save(*args, **kwargs)

        if changed:
            from apps.core.image_utils import process_image
            for field in changed:
                field_file = getattr(self, field)
                result_name = process_image(field_file, width=900, height=600, crop=True)
                if result_name != field_file.name:
                    Programme.objects.filter(pk=self.pk).update(**{field: result_name})
                    field_file.name = result_name
