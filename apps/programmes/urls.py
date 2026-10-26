from django.urls import path

from .views import ProgrammeDetailView

app_name = 'programmes'

urlpatterns = [
    path('<slug:slug>/', ProgrammeDetailView.as_view(), name='programme_detail'),
]
