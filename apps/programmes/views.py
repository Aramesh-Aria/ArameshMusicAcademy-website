from django.views.generic import DetailView

from apps.core.text import meta_description
from apps.pages.models import FAQ
from apps.schedules.week import active_sessions, session_runs
from apps.teachers.models import Instrument, Teacher

from .models import Programme


class ProgrammeDetailView(DetailView):
    template_name = 'programmes/programme_detail.html'
    context_object_name = 'programme'

    def get_queryset(self):
        return Programme.objects.active()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        programme = self.object
        context['meta_description'] = meta_description(programme.short_description)

        shown = Programme.InstrumentsShown
        context['programme_instruments'] = {
            shown.ALL: Instrument.objects.main(),
            shown.CHILDREN_ONLY: Instrument.objects.filter(children_only=True),
        }.get(programme.instruments_shown, Instrument.objects.none())

        # Who teaches it, and when: a reserved slot for a fixed-time Programme; the days its teachers are in
        # for one "with the teacher". Private lessons are every teacher on every day, so the page links to the
        # full schedule instead of listing it.
        sessions = active_sessions().order_by('weekday_order', 'start_time')
        teachers = Teacher.objects.filter(is_active=True).prefetch_related('instruments')
        if programme.kind == Programme.Kind.FIXED_TIME:
            sessions = sessions.filter(programme=programme)
            teachers = teachers.filter(class_sessions__in=sessions).distinct()
        elif programme.instruments_shown == shown.ALL:
            sessions = sessions.none()
        else:
            teachers = teachers.filter(programmes=programme)
            sessions = sessions.filter(teacher__in=teachers, programme__isnull=True)
        context['programme_teachers'] = teachers
        context['programme_sessions'] = sessions
        context['programme_runs'] = session_runs(sessions)
        context['faqs'] = FAQ.objects.active().filter(programmes=programme)
        return context
