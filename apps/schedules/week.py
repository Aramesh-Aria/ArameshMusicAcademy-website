from django.utils import timezone

from .models import ClassSession, Weekday, WEEKDAY_ORDER

# date.weekday() counts from Monday; the Academy's week starts on Saturday.
PYTHON_WEEKDAYS = [
    Weekday.MONDAY,
    Weekday.TUESDAY,
    Weekday.WEDNESDAY,
    Weekday.THURSDAY,
    Weekday.FRIDAY,
    Weekday.SATURDAY,
    Weekday.SUNDAY,
]


def today_weekday():
    """Today's Weekday in the Academy's time zone."""
    return PYTHON_WEEKDAYS[timezone.localdate().weekday()]


def week_schedule():
    """Every weekday from Saturday, each with its active sessions in start order, today flagged."""
    sessions_by_day = {weekday.value: [] for weekday in WEEKDAY_ORDER}
    sessions = (
        ClassSession.objects
        .filter(is_active=True, teacher__is_active=True)
        .select_related('teacher')
        .prefetch_related('instruments')
        .order_by('weekday_order', 'start_time', 'teacher__display_order')
    )
    for session in sessions:
        sessions_by_day[session.weekday].append(session)

    today = today_weekday()
    return [
        {
            'weekday': weekday.value,
            'label': weekday.label,
            'sessions': sessions_by_day[weekday.value],
            'is_today': weekday == today,
        }
        for weekday in WEEKDAY_ORDER
    ]
