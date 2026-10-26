from datetime import time

from django.contrib.auth import get_user_model
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.forms import modelform_factory
from django.test import TestCase, TransactionTestCase

from apps.teachers.models import Teacher

from .models import Programme

BEFORE = [
    ('programmes', '0001_initial'),
    ('teachers', '0007_instrument_page_fields_teacher_programmes'),
    ('schedules', '0007_classsession_programme'),
    ('pages', '0006_faq_and_section_keys'),
]
AFTER = [('programmes', '0002_move_subjects_out_of_instrument'), ('teachers', '0008_instrument_slug_required')]


class MoveSubjectsOutOfInstrumentTests(TransactionTestCase):
    """The data migration, run on the seed's shape: three Programmes stored as Instruments."""

    def migrate(self, targets):
        executor = MigrationExecutor(connection)
        executor.loader.build_graph()
        executor.migrate(targets)
        return executor.loader.project_state(targets).apps

    def setUp(self):
        apps = self.migrate(BEFORE)
        Instrument = apps.get_model('teachers', 'Instrument')
        Teacher = apps.get_model('teachers', 'Teacher')
        ClassSession = apps.get_model('schedules', 'ClassSession')

        names = ['سنتور', 'پیانو', 'گیتار پاپ', 'تئوری و سلفژ', 'گروه نوازی', 'موسیقی کودک', 'ساز ناشناخته']
        instrument = {name: Instrument.objects.create(name=name) for name in names}

        def teacher(first, last, *instruments):
            row = Teacher.objects.create(first_name=first, last_name=last, biography='.', profile_image='t.jpg')
            row.instruments.set(instrument[name] for name in instruments)
            return row

        def session(owner, weekday, *instruments):
            row = ClassSession.objects.create(
                teacher=owner, weekday=weekday, weekday_order=0, start_time=time(10), end_time=time(19),
            )
            row.instruments.set(instrument[name] for name in instruments)

        masoud = teacher('مسعود', 'آرامش', 'تئوری و سلفژ', 'سنتور', 'گروه نوازی')
        session(masoud, 'sat', 'تئوری و سلفژ', 'سنتور')
        session(masoud, 'thu', 'گروه نوازی')
        ali = teacher('علی', 'شمس', 'تئوری و سلفژ', 'پیانو', 'گیتار پاپ')
        session(ali, 'wed', 'تئوری و سلفژ', 'پیانو', 'گیتار پاپ')
        nasim = teacher('نسیم', 'حقی', 'موسیقی کودک')
        session(nasim, 'sat', 'موسیقی کودک')

        self.apps = self.migrate(AFTER)

    def tearDown(self):
        # Leave the database on the latest migrations for the tests that follow.
        self.migrate(MigrationExecutor(connection).loader.graph.leaf_nodes())

    def model(self, name):
        app_label = {'ClassSession': 'schedules', 'Programme': 'programmes'}.get(name, 'teachers')
        return self.apps.get_model(app_label, name)

    def test_the_four_programmes_exist_with_their_kinds(self):
        kinds = dict(self.model('Programme').objects.values_list('slug', 'kind'))

        self.assertEqual(kinds, {
            'private': 'with_teacher', 'ensemble': 'fixed_time', 'children': 'with_teacher', 'theory': 'with_teacher',
        })

    def test_the_three_fake_instruments_are_gone_and_childrens_instruments_added(self):
        instruments = dict(self.model('Instrument').objects.values_list('name', 'children_only'))

        self.assertNotIn('تئوری و سلفژ', instruments)
        self.assertNotIn('گروه نوازی', instruments)
        self.assertNotIn('موسیقی کودک', instruments)
        self.assertIs(instruments['بلز'], True)
        self.assertIs(instruments['فلوت'], True)

    def test_every_instrument_gets_a_slug_and_an_unknown_name_falls_back_to_its_pk(self):
        Instrument = self.model('Instrument')
        slugs = dict(Instrument.objects.values_list('name', 'slug'))

        self.assertEqual(slugs['سنتور'], 'santur')
        self.assertEqual(slugs['گیتار پاپ'], 'pop-guitar')
        unknown = Instrument.objects.get(name='ساز ناشناخته')
        self.assertEqual(unknown.slug, f'instrument-{unknown.pk}')

    def test_teachers_are_tagged_with_their_with_the_teacher_programmes(self):
        Teacher = self.model('Teacher')

        def programmes(last_name):
            return set(Teacher.objects.get(last_name=last_name).programmes.values_list('slug', flat=True))

        self.assertEqual(programmes('آرامش'), {'theory'})
        self.assertEqual(programmes('شمس'), {'theory'})
        self.assertEqual(programmes('حقی'), {'children'})
        nasim_instruments = Teacher.objects.get(last_name='حقی').instruments.values_list('name', flat=True)
        self.assertEqual(set(nasim_instruments), {'بلز', 'فلوت'})

    def test_the_ensemble_session_is_reserved_and_others_lose_the_fake_instruments(self):
        ClassSession = self.model('ClassSession')

        thursday = ClassSession.objects.get(teacher__last_name='آرامش', weekday='thu')
        self.assertEqual(thursday.programme.slug, 'ensemble')
        self.assertFalse(thursday.instruments.exists())

        saturday = ClassSession.objects.get(teacher__last_name='آرامش', weekday='sat')
        self.assertIsNone(saturday.programme)
        self.assertEqual(list(saturday.instruments.values_list('name', flat=True)), ['سنتور'])

        nasim = ClassSession.objects.get(teacher__last_name='حقی')
        self.assertEqual(set(nasim.instruments.values_list('name', flat=True)), {'بلز', 'فلوت'})

    def test_the_migration_reverses_to_the_original_links(self):
        apps = self.migrate(BEFORE)
        ClassSession = apps.get_model('schedules', 'ClassSession')
        Instrument = apps.get_model('teachers', 'Instrument')

        self.assertFalse(Instrument.objects.filter(name__in=['بلز', 'فلوت']).exists())
        thursday = ClassSession.objects.get(teacher__last_name='آرامش', weekday='thu')
        self.assertEqual(list(thursday.instruments.values_list('name', flat=True)), ['گروه نوازی'])
        self.assertIsNone(thursday.programme)
        saturday = ClassSession.objects.get(teacher__last_name='آرامش', weekday='sat')
        self.assertEqual(set(saturday.instruments.values_list('name', flat=True)), {'سنتور', 'تئوری و سلفژ'})
        nasim = ClassSession.objects.get(teacher__last_name='حقی')
        self.assertEqual(list(nasim.instruments.values_list('name', flat=True)), ['موسیقی کودک'])


class TeacherProgrammeChoicesTests(TestCase):
    def test_a_teacher_can_be_tagged_only_with_with_the_teacher_programmes_other_than_private_lessons(self):
        def programme(slug, kind, shown):
            return Programme.objects.create(
                name=slug, slug=slug, kind=kind, instruments_shown=shown, short_description='-', long_description='-',
            )

        programme('private', Programme.Kind.WITH_TEACHER, Programme.InstrumentsShown.ALL)
        programme('ensemble', Programme.Kind.FIXED_TIME, Programme.InstrumentsShown.NONE)
        programme('children', Programme.Kind.WITH_TEACHER, Programme.InstrumentsShown.CHILDREN_ONLY)
        programme('theory', Programme.Kind.WITH_TEACHER, Programme.InstrumentsShown.NONE)

        choices = modelform_factory(Teacher, fields=['programmes'])().fields['programmes'].queryset

        self.assertEqual(set(choices.values_list('slug', flat=True)), {'children', 'theory'})


class AdminPagesTests(TestCase):
    """Every model this step added or changed opens in the admin, listed and as a blank form."""

    def test_changelist_and_add_form_open(self):
        admin_user = get_user_model().objects.create_superuser('admin', 'admin@example.com', 'pass12345')
        self.client.force_login(admin_user)
        for path in ['programmes/programme', 'teachers/instrument', 'teachers/teacher', 'schedules/classsession', 'pages/faq']:
            for suffix in ['', 'add/']:
                with self.subTest(path=path, suffix=suffix):
                    self.assertEqual(self.client.get(f'/admin/{path}/{suffix}').status_code, 200)
