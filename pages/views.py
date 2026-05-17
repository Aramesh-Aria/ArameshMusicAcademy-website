from django.views.generic import TemplateView

from .models import SitePageContent


class PageContentMixin:
    page_key = None
    default_title = ''
    default_body = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        content = SitePageContent.objects.filter(
            page_key=self.page_key,
            is_active=True,
        ).first()
        context['page_content'] = content
        context['page_title'] = content.title if content else self.default_title
        context['page_body'] = content.body if content else self.default_body
        return context


class HomeView(PageContentMixin, TemplateView):
    template_name = 'pages/home.html'
    page_key = SitePageContent.HOME
    default_title = 'آموزشگاه موسیقی آرامش'
    default_body = 'این صفحه فعلا به عنوان نقطه شروع بک‌اند و معماری Django نگه داشته شده است.'


class AboutView(PageContentMixin, TemplateView):
    template_name = 'pages/about.html'
    page_key = SitePageContent.ABOUT
    default_title = 'درباره ما'
    default_body = 'محتوای این صفحه بعدا هنگام انتخاب قالب و آماده‌سازی متن نهایی تکمیل می‌شود.'

# Create your views here.
