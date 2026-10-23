from django.db import migrations, models
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0002_alter_teacher_date_of_birth'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='instrument',
            options={'ordering': ['name'], 'verbose_name': 'ساز', 'verbose_name_plural': 'سازها'},
        ),
        migrations.AlterModelOptions(
            name='teacher',
            options={'ordering': ['display_order', 'last_name', 'first_name'], 'verbose_name': 'استاد', 'verbose_name_plural': 'اساتید'},
        ),
        migrations.AlterField(
            model_name='instrument',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='instrument',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='نام ساز'),
        ),
        migrations.AlterField(
            model_name='instrument',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='biography',
            field=models.TextField(verbose_name='بیوگرافی'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='birth_city',
            field=models.CharField(max_length=100, verbose_name='شهر محل تولد'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='birth_province',
            field=models.CharField(max_length=100, verbose_name='استان محل تولد'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='date_of_birth',
            field=django_jalali.db.models.jDateField(verbose_name='تاریخ تولد'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='display_order',
            field=models.PositiveIntegerField(default=0, verbose_name='ترتیب نمایش'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='education',
            field=models.CharField(max_length=255, verbose_name='تحصیلات'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='first_name',
            field=models.CharField(max_length=100, verbose_name='نام'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='instruments',
            field=models.ManyToManyField(related_name='teachers', to='teachers.instrument', verbose_name='سازها'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='فعال'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='last_name',
            field=models.CharField(max_length=100, verbose_name='نام خانوادگی'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='profile_image',
            field=models.ImageField(upload_to='teachers/', verbose_name='تصویر پروفایل'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی'),
        ),
    ]
