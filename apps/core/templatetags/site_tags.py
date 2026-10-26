from django import template

register = template.Library()


@register.filter
def local_phone(number):
    """Show an Iranian number the way Visitors dial it: '+98 21 4445 7748' -> '021 4445 7748'."""
    number = str(number).strip()
    if number.startswith('+98'):
        return '0' + number[3:].strip()
    return number


@register.filter
def tel_href(number):
    """A tel: link that dials from anywhere: '+98 21 4445 7748' -> 'tel:+982144457748'."""
    return 'tel:' + ''.join(str(number).split())
