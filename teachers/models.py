from django.db import models
from django.urls import reverse
from django_jalali.db import models as jmodels


class Instrument(models.Model):
    name = models.CharField('نام ساز', max_length=100, unique=True)
    created_at = models.DateTimeField('تاریخ ایجاد', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروزرسانی', auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'ساز'
        verbose_name_plural = 'سازها'

    def __str__(self):
        return self.name


class Teacher(models.Model):
    objects = jmodels.jManager()

    first_name = models.CharField('نام', max_length=100)
    last_name = models.CharField('نام خانوادگی', max_length=100)
    instruments = models.ManyToManyField(
        Instrument,
        related_name='teachers',
        verbose_name='سازها',
    )
    date_of_birth = jmodels.jDateField('تاریخ تولد')
    birth_province = models.CharField('استان محل تولد', max_length=100)
    birth_city = models.CharField('شهر محل تولد', max_length=100)
    education = models.CharField('تحصیلات', max_length=255)
    biography = models.TextField('بیوگرافی')
    profile_image = models.ImageField('تصویر پروفایل', upload_to='teachers/')
    is_active = models.BooleanField('فعال', default=True)
    display_order = models.PositiveIntegerField('ترتیب نمایش', default=0)
    created_at = models.DateTimeField('تاریخ ایجاد', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروزرسانی', auto_now=True)

    class Meta:
        ordering = ['display_order', 'last_name', 'first_name']
        verbose_name = 'استاد'
        verbose_name_plural = 'اساتید'

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse('teachers:teacher_detail', kwargs={'pk': self.pk})
