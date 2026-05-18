from collections import defaultdict

from .models import GalleryPage


def gallery_nav_tree(request):
    pages = list(
        GalleryPage.objects
        .filter(is_active=True)
        .order_by('display_order', 'title')
        .only('id', 'title', 'slug', 'parent_id')
    )

    by_parent = defaultdict(list)
    for page in pages:
        by_parent[page.parent_id].append(page)

    def build(parent_id):
        return [
            {
                'page': page,
                'children': build(page.id),
            }
            for page in by_parent[parent_id]
        ]

    return {'gallery_nav_tree': build(None)}
