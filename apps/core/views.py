import logging

from django.http import HttpResponseServerError
from django.shortcuts import render
from django.template import loader

from .context_processors import site_info

logger = logging.getLogger(__name__)


def server_error(request):
    """The 500 page. It reads only settings, never the database, since the database may be what failed."""
    try:
        html = loader.get_template('500.html').render(site_info(request))
    except Exception:
        logger.exception('The 500 page could not be rendered')
        html = '<h1>Server Error (500)</h1>'
    return HttpResponseServerError(html)


def csrf_failure(request, reason=''):
    """A form sent with an expired or missing CSRF cookie: in practice, the contact form left open too long."""
    return render(request, '403_csrf.html', status=403)
