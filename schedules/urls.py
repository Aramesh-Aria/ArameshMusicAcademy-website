from django.urls import path

from .views import ScheduleView

app_name = 'schedules'

urlpatterns = [
    path('', ScheduleView.as_view(), name='schedule'),
]
