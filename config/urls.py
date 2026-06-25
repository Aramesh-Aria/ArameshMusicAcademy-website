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
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path
from django.views.static import serve

from core.sitemaps import sitemaps
from gallery import urls as gallery_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('teachers/', include('teachers.urls')),
    path('schedule/', include('schedules.urls')),
    path('gallery/', include(gallery_urls)),
    path('contact/', include('contact.urls')),
    path('captcha/', include('captcha.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    # Serve static files from the development directory (only locally)
    urlpatterns += static('/static/', document_root=settings.BASE_DIR / 'static_dev')

# Serve media files via Django's serve view — works regardless of DEBUG setting
# (the static() helper returns an empty list when DEBUG=False, so can't be used here)
urlpatterns += [
    re_path(r'^public/media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
