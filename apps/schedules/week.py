from dataclasses import dataclass

from django.utils import timezone

from .models import ClassSession, Weekday, WEEKDAY_ORDER

# The Academy is closed on Fridays unless a class is booked anyway.
CLOSED_DAYS = {Weekday.FRIDAY}


@dataclass(frozen=True)
class Day:
    """One weekday of the programme and its sessions."""
    weekday: str
    label: str
    sessions: list
    is_today: bool
    is_closed: bool


def today_weekday():
    """Today's Weekday in the Academy's time zone."""
    # date.weekday() counts from Monday; the Academy's week starts two days earlier, on Saturday.
    return WEEKDAY_ORDER[(timezone.localdate().weekday() + 2) % 7]


def active_sessions():
    """Every active session of an active teacher, with what `ClassSession.offerings()` reads loaded."""
    return (
        ClassSession.objects.active()
        .select_related('teacher', 'programme')
        .prefetch_related('instruments', 'teacher__programmes')
    )


def week_schedule(sessions=None):
    """Every weekday from Saturday, each with its sessions in start order, today and closed days flagged.

    `sessions` defaults to `active_sessions()`; pass them in when the caller has already fetched them.
    """
    if sessions is None:
        sessions = active_sessions()
    sessions_by_day = {weekday.value: [] for weekday in WEEKDAY_ORDER}
    for session in sorted(sessions, key=lambda s: (s.start_time, s.teacher.display_order)):
        sessions_by_day[session.weekday].append(session)

    today = today_weekday()
    return [
        Day(
            weekday=weekday.value,
            label=weekday.label,
            sessions=sessions_by_day[weekday.value],
            is_today=weekday == today,
            is_closed=weekday in CLOSED_DAYS,
        )
        for weekday in WEEKDAY_ORDER
    ]
