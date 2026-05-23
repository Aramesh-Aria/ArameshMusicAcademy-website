from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from gallery.models import GalleryPage


class GalleryRootView(TemplateView):
    template_name = 'gallery/gallery_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = None
        context['breadcrumbs'] = []
        context['child_pages'] = GalleryPage.objects.filter(
            parent__isnull=True,
            is_active=True,
        )
        context['images'] = []
        return context


class GalleryPageView(TemplateView):
    template_name = 'gallery/gallery_page.html'

    def get_context_data(self, slug_path, **kwargs):
        context = super().get_context_data(**kwargs)
        current_page = self.get_gallery_page(slug_path)
        context['current_page'] = current_page
        context['breadcrumbs'] = self.get_breadcrumbs(current_page)
        context['child_pages'] = current_page.children.filter(is_active=True)
        context['images'] = current_page.images.filter(is_active=True)
        return context

    def get_gallery_page(self, slug_path):
        parent = None
        current_page = None
        for slug in slug_path.strip('/').split('/'):
            current_page = get_object_or_404(
                GalleryPage,
                parent=parent,
                slug=slug,
                is_active=True,
            )
            parent = current_page
        return current_page

    def get_breadcrumbs(self, page):
        breadcrumbs = []
        current_page = page
        while current_page:
            breadcrumbs.append(current_page)
            current_page = current_page.parent
        return list(reversed(breadcrumbs))
