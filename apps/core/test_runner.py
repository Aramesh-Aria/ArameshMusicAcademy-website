from django.conf import settings
from django.test.runner import DiscoverRunner


class TestRunner(DiscoverRunner):
    """The default runner, with the https redirect off.

    The test client speaks plain http, so with DEBUG off every request would come back as a
    redirect to https instead of the page under test.
    """

    def setup_test_environment(self, **kwargs):
        super().setup_test_environment(**kwargs)
        settings.SECURE_SSL_REDIRECT = False
