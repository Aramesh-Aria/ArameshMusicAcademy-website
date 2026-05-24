"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('alg.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from gallery import urls as gallery_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('teachers/', include('teachers.urls')),
    path('schedule/', include('schedules.urls')),
    path('gallery/', include(gallery_urls)),
    path('contact/', include('contact.urls')),
    path('captcha/', include('captcha.urls')),
]

if settings.DEBUG:
    # Serve static files from the development directory
    urlpatterns += static('/static/', document_root=settings.BASE_DIR / 'static_dev')
    # Serve media files as configured in settings
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
