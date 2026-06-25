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
