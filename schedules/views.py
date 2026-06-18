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
            .select_related('course', 'teacher')
            .order_by(
                'course__name',
                'teacher__display_order',
                'teacher__last_name',
                'weekday_order',
                'start_time',
            )
        )
        rows_by_course_teacher = {}

        for session in sessions:
            key = (session.course_id, session.teacher_id)
            if key not in rows_by_course_teacher:
                rows_by_course_teacher[key] = {
                    'course': session.course,
                    'teacher': session.teacher,
                    'cells': {weekday.value: [] for weekday in WEEKDAY_ORDER},
                }
            rows_by_course_teacher[key]['cells'][session.weekday].append(session)

        # Group rows by course to compute rowspans and assign color indices
        all_rows = list(rows_by_course_teacher.values())
        schedule_rows = []
        color_index = 0
        i = 0
        while i < len(all_rows):
            course_id = all_rows[i]['course'].pk
            # Find how many consecutive rows share the same course
            j = i
            while j < len(all_rows) and all_rows[j]['course'].pk == course_id:
                j += 1
            span = j - i

            for k in range(i, j):
                row = all_rows[k]
                schedule_rows.append({
                    'course': row['course'],
                    'teacher': row['teacher'],
                    'show_course': k == i,
                    'course_rowspan': span if k == i else 1,
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
            i = j
            color_index += 1

        context['weekdays'] = WEEKDAY_ORDER
        context['schedule_rows'] = schedule_rows
        return context

# Create your views here.
