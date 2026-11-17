import os

from django.core.management.base import BaseCommand
from PIL import Image

from apps.core.image_utils import STORED_EXTENSION, delete_image, make_image_sizes
from apps.core.media_cleanup import file_fields, models_with_files


class Command(BaseCommand):
    help = (
        'Store the photos uploaded before uploads were stored as WebP (JPEG, mostly) as WebP too: same size in '
        'pixels, a lighter file. Each row is pointed at the new file, the old file and its srcset copies are '
        'removed, and new copies are made. A photo whose WebP would not be lighter is left as it is. Lists only; '
        'pass --convert to do it. Re-encoding costs a little quality and cannot be undone, so copy the media '
        'folder first. Safe to run again: photos already WebP are skipped.'
    )

    def add_arguments(self, parser):
        parser.add_argument('--convert', action='store_true', help='Convert the listed photos. Cannot be undone.')

    def handle(self, *args, **options):
        convert = options['convert']
        converted = kept = failed = saved = 0
        for storage, name in self.photos_to_convert():
            try:
                old_size, new_size = self.encode(storage, name, write=convert)
            except Exception as error:  # a missing or broken photo must not stop the rest
                failed += 1
                self.stderr.write(f'{name}: could not be read ({error})')
                continue
            if new_size is None:
                kept += 1
                self.stdout.write(f'{name}: left as it is (WebP would not be lighter)')
                continue
            converted += 1
            saved += old_size - new_size
            self.stdout.write(f'{name}: {old_size / 1024:.0f} KB -> {new_size / 1024:.0f} KB')

        summary = f'{converted} photos, {saved / 1024 / 1024:.1f} MB lighter as WebP; {kept} left as they are.'
        if failed:
            summary += f' Could not read {failed}.'
        if convert:
            self.stdout.write(self.style.SUCCESS(f'{summary} Converted.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'{summary} Nothing was changed; run again with --convert to do it.'))

    def photos_to_convert(self):
        """(storage, name) of every stored image that is not WebP yet, each once however many rows name it."""
        seen = set()
        for model in models_with_files():
            for field in file_fields(model):
                names = model._base_manager.exclude(**{field.name: ''}).values_list(field.name, flat=True).distinct()
                for name in sorted(n for n in names if n):
                    if name.lower().endswith(STORED_EXTENSION) or name in seen:
                        continue
                    seen.add(name)
                    yield field.storage, name

    def encode(self, storage, name, write):
        """Returns (old size, new size); new size is None when the WebP would not be lighter. Writes when asked."""
        old_abs = storage.path(name)
        old_size = os.path.getsize(old_abs)
        new_name = storage.get_available_name(os.path.splitext(name)[0] + STORED_EXTENSION)
        new_abs = storage.path(new_name)
        tmp_abs = f'{new_abs}.{os.getpid()}.tmp'
        try:
            with Image.open(old_abs) as img:
                if img.mode in ('RGBA', 'LA'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1])
                    img = background
                else:
                    img = img.convert('RGB')
                img.save(tmp_abs, 'WEBP', quality=82, method=4)
            new_size = os.path.getsize(tmp_abs)
            if new_size >= old_size:
                return old_size, None
            if write:
                os.replace(tmp_abs, new_abs)
                self.repoint(storage, name, new_name)
            return old_size, new_size
        finally:
            if os.path.exists(tmp_abs):
                os.remove(tmp_abs)

    def repoint(self, storage, old_name, new_name):
        """Every row that named the old file names the new one; the old file and its copies go; new copies are made."""
        sample = None
        for model in models_with_files():
            for field in file_fields(model):
                rows = model._base_manager.filter(**{field.name: old_name})
                first = rows.first()
                # .update(), not save(): the photo is already the right size, and no signal should fire.
                if rows.update(**{field.name: new_name}) and sample is None:
                    sample = getattr(first, field.name)
                    sample.name = new_name
        # The old copies go before the new ones are made: both are named after the same stem.
        delete_image(storage, old_name)
        if sample is not None:
            make_image_sizes(sample)
