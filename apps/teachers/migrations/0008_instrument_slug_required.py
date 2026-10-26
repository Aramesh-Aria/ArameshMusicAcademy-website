from django.db import migrations, models


class Migration(migrations.Migration):
    """Every Instrument has a slug once the data migration has filled them in."""

    dependencies = [
        ('teachers', '0007_instrument_page_fields_teacher_programmes'),
        ('programmes', '0002_move_subjects_out_of_instrument'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instrument',
            name='slug',
            field=models.SlugField(error_messages={'unique': 'ساز دیگری همین نام در آدرس را دارد.'}, help_text='با حروف لاتین، مثل santur. در آدرس صفحهٔ ساز می‌آید.', max_length=100, unique=True, verbose_name='نام در آدرس'),
        ),
    ]
