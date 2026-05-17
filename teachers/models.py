from django.db import models
from django.urls import reverse
from django_jalali.db import models as jmodels


class Instrument(models.Model):
    name = models.CharField(
        'نام ساز',
        max_length=100,
        unique=True,
        help_text='نام هر ساز را فقط یک بار ثبت کنید.',
        error_messages={
            'unique': 'این ساز قبلا ثبت شده است.',
        },
    )
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

    first_name = models.CharField('نام', max_length=100, help_text='نام استاد را وارد کنید.')
    last_name = models.CharField('نام خانوادگی', max_length=100, help_text='نام خانوادگی استاد را وارد کنید.')
    instruments = models.ManyToManyField(
        Instrument,
        related_name='teachers',
        verbose_name='سازها',
        help_text='یک یا چند ساز که این استاد تدریس می‌کند را انتخاب کنید.',
    )
    date_of_birth = jmodels.jDateField('تاریخ تولد', help_text='تاریخ تولد را به صورت شمسی وارد کنید.')
    birth_province = models.CharField('استان محل تولد', max_length=100, help_text='استان محل تولد استاد.')
    birth_city = models.CharField('شهر محل تولد', max_length=100, help_text='شهر محل تولد استاد.')
    education = models.CharField('تحصیلات', max_length=255, help_text='مدرک یا سابقه آموزشی استاد.')
    biography = models.TextField('بیوگرافی', help_text='توضیح کوتاه یا کامل درباره سابقه و فعالیت‌های استاد.')
    profile_image = models.ImageField('تصویر پروفایل', upload_to='teachers/', help_text='تصویر پرتره استاد را بارگذاری کنید.')
    is_active = models.BooleanField('فعال', default=True, help_text='فقط اساتید فعال در سایت نمایش داده می‌شوند.')
    display_order = models.PositiveIntegerField('ترتیب نمایش', default=0, help_text='عدد کمتر یعنی نمایش زودتر در لیست اساتید.')
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
