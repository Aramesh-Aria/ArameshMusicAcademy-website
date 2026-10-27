import logging
import os

from PIL import Image


def process_image(field_file, width, height, crop=False, quality=85):
    """
    Resize (and optionally center-crop) an uploaded ImageField file, saving as JPEG.

    - crop=True: center-crops to the exact width×height ratio then resizes.
    - crop=False: shrinks to fit within width×height, preserving aspect ratio (never upscales).

    Returns the new relative storage name (may differ if the original had a non-.jpg extension).
    """
    abs_path = field_file.path
    rel_name = field_file.name

    # Nothing on disk to process (e.g. a DB row pointing at a missing file) — leave the name as-is.
    if not os.path.exists(abs_path):
        return rel_name

    img = Image.open(abs_path)

    # Normalize to RGB — handles PNG transparency, CMYK camera exports, palette images, etc.
    if img.mode != 'RGB':
        if img.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])
            img = background
        else:
            img = img.convert('RGB')

    if crop:
        target_ratio = width / height
        img_ratio = img.width / img.height
        if img_ratio > target_ratio:
            # Wider than target — trim left and right
            new_w = int(img.height * target_ratio)
            left = (img.width - new_w) // 2
            img = img.crop((left, 0, left + new_w, img.height))
        elif img_ratio < target_ratio:
            # Taller than target — trim top and bottom
            new_h = int(img.width / target_ratio)
            top = (img.height - new_h) // 2
            img = img.crop((0, top, img.width, top + new_h))
        img = img.resize((width, height), Image.LANCZOS)
    else:
        # Shrink to fit; never upscale
        img.thumbnail((width, height), Image.LANCZOS)

    base_abs, _ = os.path.splitext(abs_path)
    new_abs_path = base_abs + '.jpg'
    img.save(new_abs_path, 'JPEG', quality=quality, optimize=True)

    if new_abs_path != abs_path:
        os.remove(abs_path)

    base_rel, _ = os.path.splitext(rel_name)
    return base_rel + '.jpg'


# ── Smaller copies for srcset ──
# A phone needs a few hundred pixels of a photo stored at up to 1920, so each upload is also offered at these
# widths, and at its own, as WebP (about a third lighter than the JPEG); the JPEG stays the plain `src`. The copies live under MEDIA_ROOT/sizes/, mirroring the
# original's path, and are made the first time a page asks for them; one older than its original (the admin
# replaced the photo under the same name) is made again. Nothing here may stop a page from rendering: a copy
# that can't be made is just left out, and the original is still offered.

SIZE_WIDTHS = (320, 480, 800, 1200)
SIZES_DIR = 'sizes'

logger = logging.getLogger(__name__)


def _size_name(rel_name, width):
    stem, _ = os.path.splitext(rel_name)
    return f'{SIZES_DIR}/{stem}-{width}w.webp'


def _make_size(src_abs, dest_abs, width):
    os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
    with Image.open(src_abs) as img:
        img = img.convert('RGB')
        height = round(img.height * width / img.width)
        img = img.resize((width, height), Image.LANCZOS)
        # Written aside and moved into place, so two requests making the same copy never serve half a file.
        tmp_abs = f'{dest_abs}.{os.getpid()}.tmp'
        img.save(tmp_abs, 'WEBP', quality=78, method=4)
    os.replace(tmp_abs, dest_abs)


def image_sizes(field_file):
    """[(url, width), …] for an uploaded image: its WebP copies, from the narrowest up to its own width.

    Empty when the original can't be read, so the caller falls back to a plain src.
    """
    storage = field_file.storage
    try:
        src_abs = field_file.path
        src_mtime = os.path.getmtime(src_abs)
        original_width = field_file.width
    except (OSError, ValueError, TypeError, NotImplementedError):
        return []
    if not original_width:
        return []

    sizes = []
    for width in [w for w in SIZE_WIDTHS if w < original_width] + [original_width]:
        name = _size_name(field_file.name, width)
        dest_abs = storage.path(name)
        try:
            if not os.path.exists(dest_abs) or os.path.getmtime(dest_abs) < src_mtime:
                _make_size(src_abs, dest_abs, width)
        except Exception:  # a bad upload (truncated, a decompression bomb) must not break the page
            logger.exception('Could not make the %spx copy of %s', width, field_file.name)
            if width == original_width:
                sizes.append((field_file.url, width))
            continue
        sizes.append((storage.url(name), width))
    return sizes
