from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from apps.core.text import meta_description
from apps.gallery.models import GalleryImage, GalleryPage


def with_active_images(pages):
    """Child pages with their active photos loaded, so each card's `display_cover` needs no query."""
    return pages.prefetch_related(
        Prefetch('images', queryset=GalleryImage.objects.filter(is_active=True), to_attr='active_images'),
    )


class GalleryRootView(TemplateView):
    template_name = 'gallery/gallery_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = None
        context['breadcrumbs'] = []
        context['child_pages'] = with_active_images(GalleryPage.objects.listed().filter(parent__isnull=True))
        context['images'] = []
        return context


class GalleryPageView(TemplateView):
    template_name = 'gallery/gallery_page.html'

    def get_context_data(self, slug_path, **kwargs):
        context = super().get_context_data(**kwargs)
        current_page = self.get_gallery_page(slug_path)
        context['current_page'] = current_page
        context['breadcrumbs'] = self.get_breadcrumbs(current_page)
        context['child_pages'] = with_active_images(current_page.children.filter(is_active=True))
        images = list(current_page.images.filter(is_active=True))
        current_page.active_images = images   # the og:image cover reads these instead of querying again
        context['images'] = images
        context['videos'] = current_page.videos.filter(is_active=True)
        description = current_page.description or current_page.intro_text
        if description:
            context['meta_description'] = meta_description(description)
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
            current_page.parent = parent   # already loaded: breadcrumbs and URLs walk up without a query
            parent = current_page
        return current_page

    def get_breadcrumbs(self, page):
        breadcrumbs = []
        current_page = page
        while current_page:
            breadcrumbs.append(current_page)
            current_page = current_page.parent
        return list(reversed(breadcrumbs))
