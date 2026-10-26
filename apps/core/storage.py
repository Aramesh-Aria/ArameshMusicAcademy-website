from whitenoise.storage import CompressedManifestStaticFilesStorage

# Third-party admin assets: django_jalali's datepicker CSS points at images its package does not ship,
# and jazzmin asks {% static %} for the 'vendor/bootswatch' directory, which has no manifest entry.
VENDOR_PREFIXES = ('admin/', 'vendor/')


class StaticFilesStorage(CompressedManifestStaticFilesStorage):
    """Hashed, compressed static files, strict about the site's own references.

    A vendor path that cannot be hashed is served under its plain name instead of failing.
    """

    def hashed_name(self, name, content=None, filename=None):
        try:
            return super().hashed_name(name, content, filename)
        except ValueError:  # Django's "file could not be found"
            if name.startswith(VENDOR_PREFIXES):
                return name
            raise

    def stored_name(self, name):
        try:
            return super().stored_name(name)
        except ValueError:  # Django's "missing staticfiles manifest entry"
            if name.startswith(VENDOR_PREFIXES):
                return name
            raise
