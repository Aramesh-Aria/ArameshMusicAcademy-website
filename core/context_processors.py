from django.conf import settings
from datetime import datetime

def site_info(request):
    """
    Expose site-wide contact information and current year to all templates.
    """
    from teachers.models import Instrument

    phones = getattr(settings, 'SITE_PHONES', [])
    return {
        'site_email': getattr(settings, 'SITE_EMAIL', 'info@arameshmusicacademy.com'),
        'site_phones': phones,
        'site_phone_primary': phones[0] if len(phones) > 0 else '',
        'site_address': getattr(settings, 'SITE_ADDRESS', 'تهران، خیابان نمونه، آموزشگاه موسیقی آرامش'),
        'current_year': datetime.now().year,
        'google_analytics_id': getattr(settings, 'GOOGLE_ANALYTICS_ID', ''),
        'site_instagram': getattr(settings, 'SITE_INSTAGRAM', ''),
        'site_telegram': getattr(settings, 'SITE_TELEGRAM', ''),
        'site_hours': getattr(settings, 'SITE_HOURS', []),
        'site_instruments': Instrument.objects.all(),
    }
