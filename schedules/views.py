from django.views.generic import TemplateView

from .models import ClassSession, WEEKDAY_ORDER


class ScheduleView(TemplateView):
    template_name = 'schedules/schedule.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sessions = (
            ClassSession.objects
            .filter(is_active=True, teacher__is_active=True)
            .select_related('course', 'teacher')
            .order_by('weekday_order', 'start_time')
        )
        sessions_by_weekday = {weekday.value: [] for weekday in WEEKDAY_ORDER}

        for session in sessions:
            sessions_by_weekday[session.weekday].append(session)

        context['weekday_sections'] = [
            {
                'value': weekday.value,
                'label': weekday.label,
                'sessions': sessions_by_weekday[weekday.value],
            }
            for weekday in WEEKDAY_ORDER
        ]
        return context

# Create your views here.
