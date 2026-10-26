from .models import Programme


def programme_nav(request):
    """The Programmes for the navbar's دوره‌ها menu, on every page."""
    return {'nav_programmes': Programme.objects.active().only('name', 'slug')}
