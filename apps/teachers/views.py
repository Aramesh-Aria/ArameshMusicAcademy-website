from django.db.models import Prefetch
from django.views.generic import DetailView, ListView

from apps.core.text import meta_description
from apps.schedules.models import ClassSession
from apps.schedules.week import active_sessions, session_runs

from .models import Instrument, Teacher


class TeacherListView(ListView):
    model = Teacher
    template_name = 'teachers/teacher_list.html'
    context_object_name = 'teachers'

    def get_queryset(self):
        # Each row lists the days the teacher teaches, so their active sessions come in one query.
        return (
            Teacher.objects
            .filter(is_active=True)
            .prefetch_related(
                'instruments',
                Prefetch(
                    'class_sessions',
                    queryset=ClassSession.objects.active().order_by('weekday_order', 'start_time'),
                    to_attr='active_sessions',
                ),
            )
        )


class TeacherDetailView(DetailView):
    model = Teacher
    template_name = 'teachers/teacher_detail.html'
    context_object_name = 'teacher'

    def get_queryset(self):
        return (
            Teacher.objects
            .filter(is_active=True)
            .prefetch_related('instruments', 'programmes')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = self.object
        if teacher.public_biography:
            context['meta_description'] = meta_description(teacher.public_biography)
        else:
            instruments = '، '.join(i.name for i in teacher.instruments.all())
            context['meta_description'] = (
                f'{teacher.full_name} مدرس {instruments} در آموزشگاه موسیقی آرامش.'
            )
        context['teacher_programmes'] = [p for p in teacher.programmes.all() if p.is_active]
        context['teacher_sessions'] = active_sessions().filter(teacher=teacher).order_by('weekday_order', 'start_time')
        context['teacher_runs'] = session_runs(context['teacher_sessions'], with_offerings=True)
        return context


class InstrumentListView(ListView):
    template_name = 'teachers/instrument_list.html'
    context_object_name = 'instruments'

    def get_queryset(self):
        # Children's instruments appear only on the children's Programme page and the teacher's profile.
        return Instrument.objects.main()


class InstrumentDetailView(DetailView):
    model = Instrument
    template_name = 'teachers/instrument_detail.html'
    context_object_name = 'instrument'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instrument = self.object
        if instrument.overview:
            context['meta_description'] = meta_description(instrument.overview)
        context['instrument_teachers'] = instrument.teachers.filter(is_active=True).prefetch_related('instruments')
        context['instrument_sessions'] = (
            active_sessions().filter(instruments=instrument).order_by('weekday_order', 'start_time')
        )
        context['instrument_runs'] = session_runs(context['instrument_sessions'])
        return context
