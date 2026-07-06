from django.contrib.admin.apps import AdminConfig


class ArameshAdminConfig(AdminConfig):
    """Use our custom admin site (adds the unread contact-message count) as the default."""
    default_site = 'core.admin.ArameshAdminSite'
