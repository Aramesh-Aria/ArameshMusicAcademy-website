import logging

from django.http import HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render
from django.template import loader
from django.urls import reverse

from .context_processors import site_info

logger = logging.getLogger(__name__)


def _standalone_page(request, template_name, fallback):
    """An error page built from settings alone: no database, no context processors, nothing read off the request."""
    try:
        return loader.get_template(template_name).render(site_info(request))
    except Exception:
        logger.exception('The error page %s could not be rendered', template_name)
        return fallback


def server_error(request):
    """The 500 page. It reads only settings, never the database, since the database may be what failed."""
    return HttpResponseServerError(_standalone_page(request, '500.html', '<h1>Server Error (500)</h1>'))


def bad_request(request, exception):
    """The 400 page. The request itself is what is wrong (a host that is not ours, say), so nothing is read off it."""
    return HttpResponseBadRequest(_standalone_page(request, '400.html', '<h1>Bad Request (400)</h1>'))


def csrf_failure(request, reason=''):
    """A form sent with an expired or missing CSRF cookie: the contact form, or the admin login, left open too long."""
    in_admin = request.path.startswith(reverse('admin:index'))
    return render(request, '403_csrf.html', {'in_admin': in_admin}, status=403)
