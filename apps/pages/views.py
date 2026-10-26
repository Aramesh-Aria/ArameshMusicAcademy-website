from django.conf import settings
from django.views.generic import TemplateView

from apps.gallery.models import GalleryPage
from apps.programmes.models import Programme
from apps.schedules.week import today_status, week_schedule
from apps.teachers.models import Instrument, Teacher
from apps.testimonials.models import Testimonial

from .models import FAQ, SitePageContent


def gallery_images(slug):
    """The active photos of the active top-level gallery page `slug`, in admin order; empty without one."""
    page = GalleryPage.objects.filter(slug=slug, parent__isnull=True, is_active=True).first()
    if page is None:
        return []
    return list(page.images.filter(is_active=True).select_related('gallery_page'))


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
    # The hero's headline and sentence (Gate 1 copy) until staff add the home content in the admin.
    default_title = 'موسیقی، در فضایی آرام'
    default_body = (
        'آموزش خصوصی سنتور، تار، پیانو، ویولن، آواز و سازهای دیگر برای کودکان، نوجوانان و بزرگسالان، '
        'با مدیریت مسعود آرامش، آهنگساز و نوازندهٔ سنتور.'
    )
    default_meta_description = (
        'آموزشگاه موسیقی آرامش در تهران؛ آموزش خصوصی سنتور، تار، پیانو، ویولن، آواز و سازهای دیگر برای کودکان، '
        'نوجوانان و بزرگسالان. برای انتخاب ساز و استاد با ما تماس بگیرید.'
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hero_slides'] = gallery_images(settings.HERO_GALLERY_SLUG)[:6]
        space = gallery_images(settings.ABOUT_GALLERY_SLUG)
        context['about_photo'] = space[0] if space else None
        context['gallery_preview_images'] = space[1:6]
        context['programmes'] = Programme.objects.active()
        context['instruments'] = Instrument.objects.main()
        context['home_teachers'] = Teacher.objects.filter(is_active=True).prefetch_related('instruments')[:8]
        sections = {
            content.page_key: content
            for content in SitePageContent.objects.filter(
                page_key__in=[SitePageContent.TEACHING, SitePageContent.FIRST_LESSON], is_active=True,
            )
        }
        context['teaching'] = sections.get(SitePageContent.TEACHING)
        context['first_lesson'] = sections.get(SitePageContent.FIRST_LESSON)
        context['testimonials'] = Testimonial.objects.filter(is_active=True)[:8]
        context['faqs'] = FAQ.objects.active().filter(show_on_home=True)
        context['today'] = today_status(week_schedule())
        return context


class AboutView(PageContentMixin, TemplateView):
    template_name = 'pages/about.html'
    page_key = SitePageContent.ABOUT
    default_title = 'درباره ما'
    # Shown until staff add the About content in the admin, so it is written for visitors.
    default_body = (
        'آموزشگاه موسیقی آرامش جایی برای آموختن و نواختن موسیقی ایرانی و کلاسیک است؛ '
        'برای کودکان، نوجوانان و بزرگسالان، از جلسهٔ اول تا اجرای روی صحنه.'
    )
    default_meta_description = (
        'درباره آموزشگاه موسیقی آرامش، داستان شکل‌گیری، اهداف و فضای آموزشی.'
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['space_images'] = gallery_images(settings.ABOUT_GALLERY_SLUG)
        return context
