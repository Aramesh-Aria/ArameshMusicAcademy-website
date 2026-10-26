from django.views.generic import TemplateView

from .models import WEEKDAY_ORDER
from .week import active_sessions, week_schedule
from apps.pages.views import PageContentMixin
from apps.pages.models import SitePageContent


class ScheduleView(PageContentMixin, TemplateView):
    template_name = 'schedules/schedule.html'
    page_key = SitePageContent.SCHEDULE
    default_title = 'برنامه کلاس‌ها'
    default_body = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sessions = list(active_sessions().order_by(
            'teacher__display_order',
            'teacher__last_name',
            'weekday_order',
            'start_time',
        ))

        rows_by_teacher = {}
        for session in sessions:
            row = rows_by_teacher.setdefault(session.teacher_id, {
                'teacher': session.teacher,
                'instruments': {},
                'cells': {weekday.value: [] for weekday in WEEKDAY_ORDER},
            })
            row['cells'][session.weekday].append(session)
            for instrument in session.instruments.all():
                row['instruments'][instrument.pk] = instrument

        # One fetch serves both views: the desktop table by teacher, and the week by day for phones.
        week = week_schedule(sessions)
        context['week_schedule'] = week
        context['schedule_rows'] = [
            {
                'teacher': row['teacher'],
                'instruments': sorted(row['instruments'].values(), key=lambda instrument: instrument.name),
                'cells': [
                    {'weekday': day['weekday'], 'is_today': day['is_today'], 'sessions': row['cells'][day['weekday']]}
                    for day in week
                ],
            }
            for row in rows_by_teacher.values()
        ]
        return context
