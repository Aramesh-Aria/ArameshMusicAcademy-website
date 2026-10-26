from django.db import models


class SitePageContent(models.Model):
    HOME = 'home'
    ABOUT = 'about'
    SCHEDULE = 'schedule'
    TEACHING = 'teaching'
    FIRST_LESSON = 'first_lesson'
    PAGE_CHOICES = (
        (HOME, 'خانه'),
        (ABOUT, 'درباره ما'),
        (SCHEDULE, 'برنامه کلاس‌ها'),
        (TEACHING, 'شیوهٔ آموزش (بخش صفحهٔ خانه)'),
        (FIRST_LESSON, 'سه قدم تا اولین جلسه (بخش صفحهٔ خانه)'),
    )

    page_key = models.CharField('کلید صفحه', max_length=20, choices=PAGE_CHOICES, unique=True, help_text='مشخص می‌کند این محتوا مربوط به کدام صفحه است.')
    title = models.CharField('عنوان', max_length=150, help_text='عنوان اصلی صفحه، با حروف درشت بالای صفحه. کوتاه بنویسید (حدود ۴۰ حرف)؛ توضیح بیشتر را در متن صفحه بیاورید.')
    body = models.TextField(
        'متن صفحه',
        help_text='متن اصلی که در صفحه نمایش داده می‌شود. برای «شیوهٔ آموزش» و «سه قدم تا اولین جلسه»: '
                  'هر نکته یک خط عنوان دارد و خط‌های بعدی متن آن است؛ بین نکته‌ها یک خط خالی بگذارید.',
    )
    meta_description = models.CharField(
        'توضیحات متا (سئو)',
        max_length=160,
        blank=True,
        help_text='توضیح کوتاه برای موتورهای جستجو و اشتراک‌گذاری (حداکثر ۱۶۰ کاراکتر).',
    )
    hero_image = models.ImageField(
        'تصویر اصلی صفحه',
        upload_to='pages/',
        blank=True,
        help_text='تصویر بزرگ بالای صفحه. در حال حاضر فقط برای صفحه خانه استفاده می‌شود.',
    )
    is_active = models.BooleanField('فعال', default=True, help_text='فقط محتوای فعال در صفحه عمومی استفاده می‌شود.')
    created_at = models.DateTimeField('تاریخ ایجاد', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروزرسانی', auto_now=True)

    class Meta:
        ordering = ['page_key']
        verbose_name = 'محتوای صفحه'
        verbose_name_plural = 'محتواهای صفحه'

    def __str__(self):
        return self.get_page_key_display()

    def points(self):
        """The body as (title, text) pairs: a blank line between points, the first line of each is its title."""
        points = []
        for block in self.body.replace('\r\n', '\n').split('\n\n'):
            lines = [line.strip() for line in block.strip().split('\n') if line.strip()]
            if lines:
                points.append((lines[0], ' '.join(lines[1:])))
        return points

    def save(self, *args, **kwargs):
        try:
            old = SitePageContent.objects.get(pk=self.pk)
            old_hero = old.hero_image.name if old.hero_image else None
        except SitePageContent.DoesNotExist:
            old_hero = None

        new_hero = self.hero_image.name if self.hero_image else None
        hero_changed = old_hero != new_hero

        super().save(*args, **kwargs)

        if hero_changed and self.hero_image:
            from apps.core.image_utils import process_image
            result_name = process_image(self.hero_image, width=1200, height=800, crop=True)
            if result_name != self.hero_image.name:
                SitePageContent.objects.filter(pk=self.pk).update(hero_image=result_name)
                self.hero_image.name = result_name



class FAQQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class FAQ(models.Model):
    question = models.CharField('پرسش', max_length=200)
    answer = models.TextField('پاسخ', help_text='یک خط خالی بین پاراگراف‌ها بگذارید.')
    show_on_home = models.BooleanField('نمایش در صفحهٔ خانه', default=True)
    programmes = models.ManyToManyField(
        'programmes.Programme',
        related_name='faqs',
        blank=True,
        verbose_name='دوره‌ها',
        help_text='این پرسش در صفحهٔ دوره‌هایی که انتخاب می‌کنید هم نمایش داده می‌شود.',
    )
    display_order = models.PositiveIntegerField('ترتیب نمایش', default=0, help_text='عدد کمتر یعنی نمایش زودتر.')
    is_active = models.BooleanField('فعال', default=True, help_text='فقط پرسش‌های فعال در سایت نمایش داده می‌شوند.')
    created_at = models.DateTimeField('تاریخ ایجاد', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروزرسانی', auto_now=True)

    objects = FAQQuerySet.as_manager()

    class Meta:
        ordering = ['display_order', 'pk']
        verbose_name = 'پرسش متداول'
        verbose_name_plural = 'پرسش‌های متداول'

    def __str__(self):
        return self.question
