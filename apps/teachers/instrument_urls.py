from django.urls import path

from .views import InstrumentDetailView, InstrumentListView

app_name = 'instruments'

urlpatterns = [
    path('', InstrumentListView.as_view(), name='instrument_list'),
    path('<slug:slug>/', InstrumentDetailView.as_view(), name='instrument_detail'),
]
