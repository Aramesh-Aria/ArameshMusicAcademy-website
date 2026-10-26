from dataclasses import dataclass
from datetime import time

from django.utils import timezone

from .models import ClassSession, Offerings, Weekday, WEEKDAY_ORDER

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


@dataclass(frozen=True)
class Today:
    """What the home page says about today, in the Academy's time zone.

    `state` is 'open' while today's classes run, 'over' once they have ended, and 'closed' on a day with
    none. `taught` names what is taught today; `next_label` and `next_from` say when classes resume.
    """
    state: str
    day_label: str
    taught: list
    until: time | None
    next_label: str
    next_from: time | None
    is_friday: bool


def today_status(days, now=None):
    """Today from a `week_schedule()`: what is taught until when, or when the Academy opens next."""
    now = now or timezone.localtime()
    index = next(i for i, day in enumerate(days) if day.is_today)
    today = days[index]
    until = max((s.end_time for s in today.sessions), default=None)

    taught = Offerings.combine(today.sessions).names

    following = [days[(index + step) % 7] for step in range(1, 8)]
    resume = next((day for day in following if day.sessions), None)
    if until and now.time() < until:
        state = 'open'
    else:
        state = 'over' if today.sessions else 'closed'
    return Today(
        state=state,
        day_label=today.label,
        taught=taught,
        until=until,
        next_label='فردا' if resume is following[0] else (resume.label if resume else ''),
        next_from=min(s.start_time for s in resume.sessions) if resume else None,
        is_friday=today.weekday == Weekday.FRIDAY,
    )
