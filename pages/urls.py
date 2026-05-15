from django.urls import path

from .views import AboutView, HomeView

app_name = 'pages'

urlpatterns = [
    #domain.com
    path('', HomeView.as_view(), name='home'),
    #domain.com/about
    path('about/', AboutView.as_view(), name='about'),
]
