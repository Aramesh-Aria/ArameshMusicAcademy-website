from django.conf import settings
from datetime import datetime

def site_info(request):
    """
    Expose site-wide contact information and current year to all templates.
    """
    phones = getattr(settings, 'SITE_PHONES', ['+98 21 1234 5678'])
    return {
        'site_email': getattr(settings, 'SITE_EMAIL', 'info@arameshmusicacademy.com'),
        'site_phones': phones,
        'site_phone_primary': phones[0] if phones else '',
        'site_address': getattr(settings, 'SITE_ADDRESS', 'تهران، خیابان نمونه، آموزشگاه موسیقی آرامش'),
        'current_year': datetime.now().year,
    }
