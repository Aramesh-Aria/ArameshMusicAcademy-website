from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.gallery.models import GalleryPage
from apps.programmes.models import Programme
from apps.teachers.models import Instrument, Teacher


class PublicSitemap(Sitemap):
    """Lists URLs on the public domain over https, whichever host served sitemap.xml."""
    protocol = 'https'

    def get_domain(self, site=None):
        return settings.SITE_DOMAIN


class StaticViewSitemap(PublicSitemap):
    priority = 0.7
    changefreq = 'monthly'

    def items(self):
        return [
            'pages:home',
            'pages:about',
            'schedules:schedule',
            'contact:contact',
            'teachers:teacher_list',
            'instruments:instrument_list',
            'gallery:gallery_root',
        ]

    def location(self, item):
        return reverse(item)


class TeacherSitemap(PublicSitemap):
    priority = 0.6
    changefreq = 'monthly'

    def items(self):
        return Teacher.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class GalleryPageSitemap(PublicSitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return GalleryPage.objects.listed()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class ProgrammeSitemap(PublicSitemap):
    priority = 0.7
    changefreq = 'monthly'

    def items(self):
        return Programme.objects.active()

    def lastmod(self, obj):
        return obj.updated_at


class InstrumentSitemap(PublicSitemap):
    priority = 0.6
    changefreq = 'monthly'

    def items(self):
        return Instrument.objects.main()

    def lastmod(self, obj):
        return obj.updated_at


sitemaps = {
    'static': StaticViewSitemap,
    'programmes': ProgrammeSitemap,
    'instruments': InstrumentSitemap,
    'teachers': TeacherSitemap,
    'gallery': GalleryPageSitemap,
}
