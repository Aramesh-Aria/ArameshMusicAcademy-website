from django.db.models import Prefetch
from django.views.generic import DetailView, ListView

from apps.schedules.models import ClassSession

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
            .prefetch_related('instruments')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = self.object
        if teacher.biography:
            context['meta_description'] = ' '.join(teacher.biography.split())[:160]
        else:
            instruments = '، '.join(i.name for i in teacher.instruments.all())
            context['meta_description'] = (
                f'{teacher.full_name} مدرس {instruments} در آموزشگاه موسیقی آرامش.'
            )
        context['teacher_sessions'] = (
            teacher.class_sessions.active()
            .select_related('teacher', 'programme')
            .prefetch_related('instruments', 'teacher__programmes')
            .order_by('weekday_order', 'start_time')
        )
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
            context['meta_description'] = ' '.join(instrument.overview.split())[:160]
        context['instrument_teachers'] = instrument.teachers.filter(is_active=True)
        return context
