"""Move theory, ensemble playing and children's music out of Instrument and into Programme (ADR-0002).

Every lookup is by name and skips quietly when the row is missing, because production data may differ
from the seed. The reverse puts the three fake Instruments and their links back.
"""
from django.db import migrations

PRIVATE = 'کلاس خصوصی'
ENSEMBLE = 'گروه نوازی'
CHILDREN = 'موسیقی کودک'
THEORY = 'تئوری و سلفژ'
SUBJECTS = (THEORY, ENSEMBLE, CHILDREN)

PROGRAMMES = [
    {
        'name': PRIVATE,
        'slug': 'private',
        'kind': 'with_teacher',
        'instruments_shown': 'all',
        'display_order': 1,
        'short_description': (
            'سنتور، تار، سه‌تار، پیانو، ویولن، گیتار، آواز و سازهای کوبه‌ای؛ '
            'یک استاد و یک هنرجو، متناسب با سطح و هدف هر هنرجو.'
        ),
        'long_description': (
            'در آموزشگاه آرامش هر کلاس خصوصی است: یک استاد و یک هنرجو، و برنامه‌ای که با سطح و هدف همان هنرجو پیش می‌رود.\n\n'
            'می‌توانید موسیقی اصیل ایرانی بیاموزید (سنتور، تار، سه‌تار، تنبک، دف و آواز ایرانی)، یا پیانو، ویولن، گیتار، '
            'آکوردئون و سازهای کوبه‌ای دیگر. استادان آرامش بیشترشان سابقهٔ اجرا در کنسرت‌ها و جشنواره‌ها دارند و ردیف و ساز را '
            'نزد استادان شناخته‌شده آموخته‌اند.\n\n'
            'برای انتخاب ساز و استاد، با آموزشگاه تماس بگیرید.'
        ),
    },
    {
        'name': ENSEMBLE,
        'slug': 'ensemble',
        'kind': 'fixed_time',
        'instruments_shown': 'none',
        'display_order': 2,
        'short_description': 'پنجشنبه‌ها هنرجویان کنار کلاس خصوصی‌شان با هم می‌نوازند، با سرپرستی مسعود آرامش.',
        'long_description': (
            'گروه نوازی جایی است که هنرجویان آرامش، کنار کلاس خصوصی‌شان، با هم می‌نوازند. کلاس‌های گروه نوازی ویژهٔ کودکان، '
            'نوجوانان و بزرگسالان است و پنجشنبه‌ها با سرپرستی مسعود آرامش برگزار می‌شود؛ او پیش‌تر سرپرست ارکستر جوانان یزد '
            'و گروه نوا بوده است.\n\n'
            'در ساعت گروه نوازی کلاس دیگری برگزار نمی‌شود.'
        ),
    },
    {
        'name': CHILDREN,
        'slug': 'children',
        'kind': 'with_teacher',
        'instruments_shown': 'children_only',
        'display_order': 3,
        'short_description': (
            'آشنایی کودکان با نت و ریتم و نواختن سازهای کودک مانند بلز و فلوت، نزد نسیم حقی، '
            'مدرس موسیقی کودک با دوره‌های روش ارف.'
        ),
        'long_description': (
            'در کلاس موسیقی کودک، کودکان با نت‌خوانی پایه آشنا می‌شوند و سازهای کودک مانند بلز و فلوت را می‌نوازند.\n\n'
            'مدرس این کلاس، نسیم حقی، سال‌هاست به کودکان و نوجوانان موسیقی آموزش می‌دهد، دوره‌های موسیقی کودک به روش ارف را '
            'گذرانده و کارت صلاحیت تدریس موسیقی کودک از وزارت فرهنگ و ارشاد اسلامی دارد. در کلاس‌های او آموزش اصولی موسیقی '
            'با پرورش خلاقیت کودکان همراه است.'
        ),
    },
    {
        'name': THEORY,
        'slug': 'theory',
        'kind': 'with_teacher',
        'instruments_shown': 'none',
        'display_order': 4,
        'short_description': 'خواندن نت، ریتم و شنیدن موسیقی، نزد مسعود آرامش و علی شمس، در همان روزهایی که در آموزشگاه هستند.',
        'long_description': (
            'تئوری و سلفژ زبان مشترک همهٔ سازهاست: خواندن نت، ریتم و شنیدن دقیق. این کلاس را مسعود آرامش و علی شمس درس '
            'می‌دهند، در همان روزهایی که در آموزشگاه حضور دارند؛ برای زمانش با آموزشگاه هماهنگ کنید.'
        ),
    },
]

# Slugs, in display order, for the Instruments the Academy teaches today (gate-1-models-and-copy.md § 1.2).
INSTRUMENT_SLUGS = {
    'سنتور': 'santur',
    'تار': 'tar',
    'سه تار': 'setar',
    'پیانو': 'piano',
    'ویولن': 'violin',
    'آواز ایرانی': 'persian-voice',
    'تنبک': 'tombak',
    'دف': 'daf',
    'داربوکا': 'darbuka',
    'هنگدرام': 'handpan',
    'کاخن': 'cajon',
    'آکوردئون': 'accordion',
    'هارمونیکا': 'harmonica',
    'گیتار الکتریک': 'electric-guitar',
    'گیتار پاپ': 'pop-guitar',
}
CHILDREN_INSTRUMENTS = {'بلز': 'glockenspiel', 'فلوت': 'flute'}


def forwards(apps, schema_editor):
    Programme = apps.get_model('programmes', 'Programme')
    Instrument = apps.get_model('teachers', 'Instrument')
    Teacher = apps.get_model('teachers', 'Teacher')
    ClassSession = apps.get_model('schedules', 'ClassSession')

    # A fresh database (tests, a new install) has nothing to move; seed_sample_data fills it.
    if not Instrument.objects.exists():
        return

    programmes = {}
    for data in PROGRAMMES:
        fields = dict(data)
        name = fields.pop('name')
        programmes[name], _ = Programme.objects.get_or_create(name=name, defaults=fields)

    for order, (name, slug) in enumerate(INSTRUMENT_SLUGS.items(), start=1):
        Instrument.objects.filter(name=name).update(slug=slug, display_order=order)
    for instrument in Instrument.objects.filter(slug__isnull=True).exclude(name__in=SUBJECTS):
        instrument.slug = f'instrument-{instrument.pk}'
        instrument.save(update_fields=['slug'])

    subjects = {instrument.name: instrument for instrument in Instrument.objects.filter(name__in=SUBJECTS)}

    # Teachers who taught theory or children's music now offer that Programme "with the teacher".
    for name in (THEORY, CHILDREN):
        if name in subjects:
            for teacher in Teacher.objects.filter(instruments=subjects[name]):
                teacher.programmes.add(programmes[name])

    # A session that taught only ensemble playing is reserved for it, and teaches nothing else.
    if ENSEMBLE in subjects:
        for session in ClassSession.objects.filter(instruments=subjects[ENSEMBLE]):
            if set(session.instruments.values_list('name', flat=True)) == {ENSEMBLE}:
                session.programme = programmes[ENSEMBLE]
                session.save(update_fields=['programme'])
                session.instruments.clear()

    # Children's music is now taught on the children's instruments. They are children-only, so the
    # schedule still reads «موسیقی کودک» for those sessions, from the teacher's Programme.
    children_teachers = list(Teacher.objects.filter(programmes=programmes[CHILDREN]))
    children_sessions = (
        list(ClassSession.objects.filter(instruments=subjects[CHILDREN])) if CHILDREN in subjects else []
    )
    for order, (name, slug) in enumerate(CHILDREN_INSTRUMENTS.items(), start=len(INSTRUMENT_SLUGS) + 1):
        instrument, _ = Instrument.objects.get_or_create(
            name=name, defaults={'slug': slug, 'children_only': True, 'display_order': order},
        )
        for owner in children_teachers + children_sessions:
            owner.instruments.add(instrument)

    # Deleting the rows also removes them from every remaining Teacher and ClassSession.
    for instrument in subjects.values():
        instrument.delete()


def backwards(apps, schema_editor):
    Programme = apps.get_model('programmes', 'Programme')
    Instrument = apps.get_model('teachers', 'Instrument')
    ClassSession = apps.get_model('schedules', 'ClassSession')

    for name in SUBJECTS:
        programme = Programme.objects.filter(name=name).first()
        if programme is None:
            continue
        instrument, _ = Instrument.objects.get_or_create(name=name)
        for session in ClassSession.objects.filter(programme=programme):
            session.programme = None
            session.save(update_fields=['programme'])
            session.instruments.add(instrument)
        for teacher in programme.teachers.all():
            teacher.instruments.add(instrument)
            for session in ClassSession.objects.filter(teacher=teacher, programme__isnull=True):
                session.instruments.add(instrument)

    Instrument.objects.filter(name__in=CHILDREN_INSTRUMENTS, children_only=True).delete()
    Programme.objects.filter(name__in=[data['name'] for data in PROGRAMMES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('programmes', '0001_initial'),
        ('teachers', '0007_instrument_page_fields_teacher_programmes'),
        ('schedules', '0007_classsession_programme'),
        ('pages', '0006_faq_and_section_keys'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
