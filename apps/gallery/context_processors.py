from collections import defaultdict

from django.utils.functional import SimpleLazyObject

from .models import GalleryPage


def build_nav_tree():
    pages = list(
        GalleryPage.objects
        .listed()
        .order_by('display_order', 'title')
        .only('id', 'title', 'slug', 'parent_id')
    )

    by_parent = defaultdict(list)
    for page in pages:
        by_parent[page.parent_id].append(page)

    def build(parent):
        children = by_parent[parent.id if parent else None]
        for page in children:
            # The parent is already loaded: a child's URL walks up to it without a query of its own.
            page.parent = parent
        return [{'page': page, 'children': build(page)} for page in children]

    return build(None)


def gallery_nav_tree(request):
    # Lazy, so a page that never shows the menu (the admin) never runs the query.
    return {'gallery_nav_tree': SimpleLazyObject(build_nav_tree)}
