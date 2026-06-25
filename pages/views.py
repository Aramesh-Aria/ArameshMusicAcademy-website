from django.conf import settings
from django.views.generic import TemplateView

from gallery.models import GalleryImage, GalleryPage
from teachers.models import Teacher
from testimonials.models import Testimonial

from .models import SitePageContent


class PageContentMixin:
    page_key = None
    default_title = ''
    default_body = ''
    default_meta_description = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        content = SitePageContent.objects.filter(
            page_key=self.page_key,
            is_active=True,
        ).first()
        context['page_content'] = content
        context['page_title'] = content.title if content else self.default_title
        context['page_body'] = content.body if content else self.default_body
        context['meta_description'] = (
            content.meta_description if content and content.meta_description
            else self.default_meta_description
        )
        context['page_hero_image'] = (
            content.hero_image if content and content.hero_image else None
        )
        return context


class HomeView(PageContentMixin, TemplateView):
    template_name = 'pages/home.html'
    page_key = SitePageContent.HOME
    default_title = 'آموزشگاه موسیقی آرامش'
    default_body = 'این صفحه فعلا به عنوان نقطه شروع بک‌اند و معماری Django نگه داشته شده است.'
    default_meta_description = (
        'آموزشگاه موسیقی آرامش؛ آموزش تخصصی سازهای مختلف توسط اساتید مجرب. '
        'برای مشاوره و ثبت‌نام با ما در تماس باشید.'
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_teachers'] = (
            Teacher.objects
            .filter(is_active=True)
            .prefetch_related('instruments')[:3]
        )
        context['gallery_preview_images'] = (
            GalleryImage.objects
            .filter(is_active=True, gallery_page__is_active=True)
            .select_related('gallery_page')
            .order_by('-created_at')[:6]
        )
        context['testimonials'] = Testimonial.objects.filter(is_active=True)
        return context


class AboutView(PageContentMixin, TemplateView):
    template_name = 'pages/about.html'
    page_key = SitePageContent.ABOUT
    default_title = 'درباره ما'
    default_body = 'محتوای این صفحه بعدا هنگام انتخاب قالب و آماده‌سازی متن نهایی تکمیل می‌شود.'
    default_meta_description = (
        'درباره آموزشگاه موسیقی آرامش، داستان شکل‌گیری، اهداف و فضای آموزشی.'
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        space_page = (
            GalleryPage.objects
            .filter(slug=settings.ABOUT_GALLERY_SLUG, is_active=True)
            .first()
        )
        context['space_images'] = (
            space_page.images.filter(is_active=True) if space_page else GalleryImage.objects.none()
        )
        return context
