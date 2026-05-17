from django.urls import path

from .views import GalleryPageView, GalleryRootView

app_name = 'gallery'

urlpatterns = [
    path('', GalleryRootView.as_view(), name='gallery_root'),
    path('<path:slug_path>/', GalleryPageView.as_view(), name='gallery_detail'),
]
