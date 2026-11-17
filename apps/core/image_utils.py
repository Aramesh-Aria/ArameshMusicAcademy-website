import logging
import os
import queue
import threading

from django.db import transaction
from PIL import Image

# Every upload is stored as WebP: a third lighter than the JPEG it replaced, and read by every browser since 2020.
# Photos stored before this (JPEG) stay as they are until they are replaced.
STORED_EXTENSION = '.webp'


def process_image(field_file, width, height, crop=False, quality=82):
    """
    Resize (and optionally center-crop) an uploaded ImageField file and store it as WebP, whatever was uploaded.

    - crop=True: center-crops to the exact width×height ratio then resizes.
    - crop=False: shrinks to fit within width×height, preserving aspect ratio (never upscales).

    Returns the new relative storage name: the upload's, with `.webp`. The upload itself is removed.
    """
    storage = field_file.storage
    abs_path = field_file.path
    rel_name = field_file.name

    # Nothing on disk to process (e.g. a DB row pointing at a missing file) — leave the name as-is.
    if not os.path.exists(abs_path):
        return rel_name

    with Image.open(abs_path) as upload:
        img = upload
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

        # Storage gave the upload a name no other file has, but only with the upload's own extension: «a.jpg» is
        # free while another row's «a.webp» is on disk. So the WebP name is asked for too, or it would overwrite
        # that row's photo.
        new_name = os.path.splitext(rel_name)[0] + STORED_EXTENSION
        if new_name != rel_name:
            new_name = storage.get_available_name(new_name)
        new_abs_path = storage.path(new_name)
        # Written aside and moved into place, so a page never serves half a file.
        tmp_abs_path = f'{new_abs_path}.{os.getpid()}.tmp'
        img.save(tmp_abs_path, 'WEBP', quality=quality, method=4)
        os.replace(tmp_abs_path, new_abs_path)

    if new_abs_path != abs_path:
        os.remove(abs_path)
    return new_name


# ── Smaller copies for srcset ──
# A phone needs a few hundred pixels of a photo stored at up to 1920, so each upload is also offered at these
# widths as WebP. A photo stored as JPEG (uploaded before uploads were stored as WebP) gets a WebP copy at its
# own width too, and stays the plain `src`; a WebP photo is its own widest copy. The
# copies live under MEDIA_ROOT/sizes/, mirroring the original's path. They are made after an upload is saved,
# never while a page renders: a page only offers the copies already on disk and no older than their original
# (the admin may replace a photo under the same name), so a missing one costs a heavier photo, not a slow page.
# `manage.py make_image_sizes` makes any that are missing.

SIZE_WIDTHS = (320, 480, 800, 1200)
SIZES_DIR = 'sizes'

logger = logging.getLogger(__name__)


def _size_name(rel_name, width):
    stem, _ = os.path.splitext(rel_name)
    return f'{SIZES_DIR}/{stem}-{width}w.webp'


def _is_size_copy(rel_name, original_name):
    """Whether rel_name is one of original_name's copies (`<stem>-<width>w.webp`, not a longer stem's)."""
    stem = os.path.splitext(original_name)[0]
    prefix = f'{SIZES_DIR}/{stem}-'
    rest = rel_name[len(prefix):]
    return rel_name.startswith(prefix) and rest.endswith('w.webp') and rest[:-len('w.webp')].isdigit()


def _widths(rel_name, original_width):
    """The widths copies are made at: the steps narrower than the photo, and its own unless it is WebP already."""
    narrower = [w for w in SIZE_WIDTHS if w < original_width]
    return narrower if rel_name.lower().endswith(STORED_EXTENSION) else narrower + [original_width]


def _is_fresh(dest_abs, src_mtime):
    try:
        return os.path.getmtime(dest_abs) >= src_mtime
    except OSError:
        return False


def image_sizes(field_file):
    """[(url, width), …] for an uploaded image: its WebP copies already made, from the narrowest up to its own width.

    Never makes a copy. When some are made but not the one at the photo's own width, the original stands in for it.
    Empty when there are none or the original can't be read, so the caller falls back to a plain src.
    """
    storage = field_file.storage
    try:
        src_mtime = os.path.getmtime(field_file.path)
        original_width = field_file.width
    except (OSError, ValueError, TypeError, NotImplementedError):
        return []
    if not original_width:
        return []

    sizes = []
    for width in _widths(field_file.name, original_width):
        name = _size_name(field_file.name, width)
        if _is_fresh(storage.path(name), src_mtime):
            sizes.append((storage.url(name), width))
    # The photo itself is the widest choice: when it is WebP, or when its own-width copy is not made yet.
    if sizes and sizes[-1][1] != original_width:
        sizes.append((field_file.url, original_width))
    return sizes


def make_image_sizes(field_file):
    """Make the copies of an uploaded image that are missing or older than it. Returns how many were made.

    Raises when the original can't be read; the callers log it and go on.
    """
    storage, name = field_file.storage, field_file.name
    src_abs = storage.path(name)
    src_mtime = os.path.getmtime(src_abs)
    with Image.open(src_abs) as img:
        original_width, original_height = img.size
        copies = [(width, storage.path(_size_name(name, width))) for width in _widths(name, original_width)]
        stale = [(width, dest_abs) for width, dest_abs in copies if not _is_fresh(dest_abs, src_mtime)]
        if not stale:
            return 0

        def height(width):
            return round(original_height * width / original_width)

        # Decoded once for every copy. A JPEG decodes straight at 1/2, 1/4 or 1/8 scale when the widest copy
        # still needed allows it, and reducing_gap shrinks by whole factors before the LANCZOS pass: both far
        # cheaper than a LANCZOS resize of the whole photo, with no visible loss at these sizes.
        widest = max(width for width, _ in stale)
        img.draft('RGB', (widest, height(widest)))
        img = img.convert('RGB')
        for width, dest_abs in stale:
            copy = img.resize((width, height(width)), Image.LANCZOS, reducing_gap=3.0)
            os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
            # Written aside and moved into place, so a page never offers half a file.
            tmp_abs = f'{dest_abs}.{os.getpid()}.tmp'
            copy.save(tmp_abs, 'WEBP', quality=78, method=4)
            os.replace(tmp_abs, dest_abs)
    return len(stale)


# ── Making copies after an upload ──
# A model calls schedule_image_sizes() from save(); once the save commits, the upload goes on a queue that one
# daemon thread per process works through, behind the admin's response. Runflare runs only gunicorn and nginx,
# so there is no Celery or cron to hand this to (ADR-0003). One thread, not one per upload, so a gallery of
# twenty photos is resized one at a time instead of twenty at once on a small container. A job lost with its
# worker (gunicorn restarted it) leaves only the photo itself on the page; `manage.py make_image_sizes` catches up.

_jobs = queue.Queue()
_worker = None
_worker_lock = threading.Lock()


def _work():
    while True:
        field_file = _jobs.get()
        try:
            make_image_sizes(field_file)
        except Exception:  # a bad upload (truncated, a decompression bomb) must not stop the next one
            logger.exception('Could not make the copies of %s', field_file.name)
        finally:
            _jobs.task_done()


def _enqueue(field_file):
    global _worker
    with _worker_lock:
        # Also after a fork: the child process inherits the queue but not the thread.
        if _worker is None or not _worker.is_alive():
            _worker = threading.Thread(target=_work, name='image-sizes', daemon=True)
            _worker.start()
    _jobs.put(field_file)


def schedule_image_sizes(field_file):
    """Make an upload's copies in the background, once the save that stored it has committed."""
    transaction.on_commit(lambda: _enqueue(field_file))


def wait_for_image_sizes():
    """Block until every scheduled copy is made: for commands, which would otherwise exit with the thread."""
    _jobs.join()


# ── Removing a photo nobody shows any more ──

def delete_image(storage, name):
    """Remove a stored file and its srcset copies from disk. A file already gone is not an error."""
    paths = [storage.path(name)]
    sizes_dir = os.path.dirname(storage.path(_size_name(name, 0)))
    if os.path.isdir(sizes_dir):
        rel_dir = os.path.dirname(_size_name(name, 0))
        paths += [
            os.path.join(sizes_dir, entry) for entry in os.listdir(sizes_dir)
            if _is_size_copy(f'{rel_dir}/{entry}', name)
        ]
    for path in paths:
        try:
            os.remove(path)
        except FileNotFoundError:
            pass
