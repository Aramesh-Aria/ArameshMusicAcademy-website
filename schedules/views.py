from django.views.generic import TemplateView

from .models import ClassSession, WEEKDAY_ORDER
from pages.views import PageContentMixin
from pages.models import SitePageContent


class ScheduleView(PageContentMixin, TemplateView):
    template_name = 'schedules/schedule.html'
    page_key = SitePageContent.SCHEDULE
    default_title = 'برنامه کلاس‌ها'
    default_body = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sessions = (
            ClassSession.objects
            .filter(is_active=True, teacher__is_active=True)
            .select_related('teacher')
            .prefetch_related('instruments')
            .order_by(
                'teacher__display_order',
                'teacher__last_name',
                'weekday_order',
                'start_time',
            )
        )

        rows_by_teacher = {}
        for session in sessions:
            key = session.teacher_id
            if key not in rows_by_teacher:
                rows_by_teacher[key] = {
                    'teacher': session.teacher,
                    'instruments': {},
                    'cells': {weekday.value: [] for weekday in WEEKDAY_ORDER},
                }
            rows_by_teacher[key]['cells'][session.weekday].append(session)
            for instrument in session.instruments.all():
                rows_by_teacher[key]['instruments'][instrument.pk] = instrument

        schedule_rows = []
        for color_index, row in enumerate(rows_by_teacher.values()):
            instruments = sorted(
                row['instruments'].values(),
                key=lambda instrument: instrument.name,
            )
            schedule_rows.append({
                'teacher': row['teacher'],
                'instruments': instruments,
                'color_index': color_index % 6,
                'cells': [
                    {
                        'weekday': weekday.value,
                        'label': weekday.label,
                        'sessions': row['cells'][weekday.value],
                    }
                    for weekday in WEEKDAY_ORDER
                ],
            })

        context['weekdays'] = WEEKDAY_ORDER
        context['schedule_rows'] = schedule_rows
        return context
