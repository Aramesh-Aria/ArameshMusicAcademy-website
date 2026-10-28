from django import template
from django.utils.html import format_html

from apps.core.image_utils import image_sizes

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
    """Persian digits for text whose face draws ASCII digits as Latin: '404' -> '۴۰۴'.

    Sahel needs no filter: the site loads its Farsi-Digits build, and it also draws the digits in
    IranNastaliq display text, whose file leaves them out. Keep tel: links and other machine
    values in ASCII; this is for what the Visitor reads.
    """
    return str(value).translate(PERSIAN_DIGITS)


@register.filter
def clock(value):
    """A time as a clock reading for a sentence: 21:00 -> '21', 9:30 -> '9:30'."""
    if not value:
        return ''
    return str(value.hour) if not value.minute else f'{value.hour}:{value.minute:02d}'


@register.simple_tag
def image_size(field):
    """`width` and `height` attributes for an uploaded image, so the page keeps its place while it loads.

    Empty when the file can't be read (missing from media, or not an image): the photo then just loads
    without them, rather than the page failing.
    """
    try:
        width, height = field.width, field.height
    except (OSError, ValueError, TypeError):
        return ''
    if not width or not height:
        return ''
    return format_html('width="{}" height="{}"', width, height)


@register.simple_tag
def srcset(field, sizes, attr='srcset'):
    """`srcset` and `sizes` attributes offering an uploaded image's smaller copies (see `image_utils.image_sizes`).

    `sizes` says how wide the photo is drawn, as in HTML; for a photo cropped with `object-fit: cover`, give the
    width its crop needs, not its box's. Pass attr='data-srcset' for a photo that waits in `data-src`. Empty while
    no copy has been made, so the plain `src` stands alone; the tag never makes one, so a page stays fast.
    """
    candidates = image_sizes(field)
    if not candidates:
        return ''
    value = ', '.join(f'{url} {width}w' for url, width in candidates)
    return format_html('{}="{}" sizes="{}"', attr, value, sizes)
