import django.db.models.deletion
from django.db import migrations, models
from django.utils import timezone


WEEKDAY_SORT_VALUES = {
    'sat': 0,
    'sun': 1,
    'mon': 2,
    'tue': 3,
    'wed': 4,
    'thu': 5,
    'fri': 6,
}


def populate_course_timestamps(apps, schema_editor):
    Course = apps.get_model('schedules', 'Course')
    now = timezone.now()
    Course.objects.filter(created_at__isnull=True).update(created_at=now)
    Course.objects.filter(updated_at__isnull=True).update(updated_at=now)


def populate_weekday_order(apps, schema_editor):
    ClassSession = apps.get_model('schedules', 'ClassSession')
    for session in ClassSession.objects.all():
        session.weekday_order = WEEKDAY_SORT_VALUES[session.weekday]
        session.save(update_fields=['weekday_order'])


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AddField(
            model_name='course',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='تاریخ بروزرسانی'),
        ),
        migrations.AddField(
            model_name='classsession',
            name='weekday_order',
            field=models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='ترتیب روز هفته'),
        ),
        migrations.RunPython(populate_course_timestamps, migrations.RunPython.noop),
        migrations.RunPython(populate_weekday_order, migrations.RunPython.noop),
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['name'], 'verbose_name': 'کلاس', 'verbose_name_plural': 'کلاس‌ها'},
        ),
        migrations.AlterModelOptions(
            name='classsession',
            options={'ordering': ['weekday_order', 'start_time', 'teacher__last_name'], 'verbose_name': 'جلسه کلاس', 'verbose_name_plural': 'جلسه‌های کلاس'},
        ),
        migrations.AlterField(
            model_name='classsession',
            name='capacity',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='ظرفیت'),
        ),
        migrations.AlterField(
            model_name='classsession',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='class_sessions', to='schedules.course', verbose_name='کلاس'),
        ),
        migrations.AlterField(
            model_name='classsession',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='classsession',
            name='end_time',
            field=models.TimeField(verbose_name='ساعت پایان'),
        ),
        migrations.AlterField(
            model_name='classsession',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='فعال'),
        ),
        migrations.AlterField(
            model_name='classsession',
            name='notes',
            field=models.TextField(blank=True, verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='classsession',
            name='start_time',
            field=models.TimeField(verbose_name='ساعت شروع'),
        ),
        migrations.AlterField(
            model_name='classsession',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='class_sessions', to='teachers.teacher', verbose_name='استاد'),
        ),
        migrations.AlterField(
            model_name='classsession',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی'),
        ),
        migrations.AlterField(
            model_name='classsession',
            name='weekday',
            field=models.CharField(choices=[('sat', 'شنبه'), ('sun', 'یکشنبه'), ('mon', 'دوشنبه'), ('tue', 'سه\u200cشنبه'), ('wed', 'چهارشنبه'), ('thu', 'پنجشنبه'), ('fri', 'جمعه')], max_length=3, verbose_name='روز هفته'),
        ),
        migrations.AlterField(
            model_name='course',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=120, unique=True, verbose_name='نام کلاس'),
        ),
        migrations.AlterField(
            model_name='course',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی'),
        ),
    ]
