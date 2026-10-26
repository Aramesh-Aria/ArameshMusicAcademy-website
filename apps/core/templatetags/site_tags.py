from django import template

register = template.Library()

PERSIAN_DIGITS = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')


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


@register.filter
def fa_digits(value):
    """Persian digits for text set in Amiri, which draws ASCII digits as Latin: '404' -> '۴۰۴'.

    Sahel needs no filter: the site loads its Farsi-Digits build. Keep tel: links and other machine
    values in ASCII; this is for what the Visitor reads.
    """
    return str(value).translate(PERSIAN_DIGITS)
