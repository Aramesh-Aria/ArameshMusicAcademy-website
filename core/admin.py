from django.contrib import admin


class ArameshAdminSite(admin.AdminSite):
    """Default admin site that shows the unread contact-message count in the sidebar."""

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, app_label)

        try:
            from contact.models import ContactMessage
            unread = ContactMessage.objects.filter(is_read=False).count()
        except Exception:
            unread = 0

        if unread:
            for app in app_list:
                for model in app.get('models', []):
                    if model.get('object_name') == 'ContactMessage':
                        model['name'] = f"{model['name']} ({unread})"

        return app_list
