from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from gallery.models import GalleryPage
from teachers.models import Teacher


class StaticViewSitemap(Sitemap):
    priority = 0.7
    changefreq = 'monthly'

    def items(self):
        return [
            'pages:home',
            'pages:about',
            'schedules:schedule',
            'contact:contact',
            'teachers:teacher_list',
            'gallery:gallery_root',
        ]

    def location(self, item):
        return reverse(item)


class TeacherSitemap(Sitemap):
    priority = 0.6
    changefreq = 'monthly'

    def items(self):
        return Teacher.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class GalleryPageSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return GalleryPage.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


sitemaps = {
    'static': StaticViewSitemap,
    'teachers': TeacherSitemap,
    'gallery': GalleryPageSitemap,
}
