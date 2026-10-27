from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import models

from apps.core.image_utils import make_image_sizes


class Command(BaseCommand):
    help = (
        'Make the srcset copies of every uploaded photo that are missing or older than their photo. Uploads get '
        'theirs in the background; this catches up after a worker died mid-way, or after a deploy that touched '
        'images. Copies already up to date are skipped, so it is safe to run again.'
    )

    def handle(self, *args, **options):
        files = list(self.uploaded_images())
        made = failed = 0
        for number, field_file in enumerate(files, 1):
            prefix = f'[{number}/{len(files)}] {field_file.name}'
            try:
                count = make_image_sizes(field_file)
            except Exception as error:  # a bad upload must not stop the rest
                failed += 1
                self.stderr.write(f'{prefix}: could not be read ({error})')
                continue
            made += count
            self.stdout.write(f'{prefix}: {count} made' if count else f'{prefix}: up to date')

        summary = f'{made} copies made for {len(files)} photos.'
        if failed:
            self.stdout.write(self.style.WARNING(f'{summary} Could not read {failed} of them.'))
        else:
            self.stdout.write(self.style.SUCCESS(summary))

    def uploaded_images(self):
        for model in apps.get_models():
            if not model.__module__.startswith('apps.'):
                continue
            for field in model._meta.get_fields():
                if not isinstance(field, models.ImageField):
                    continue
                for obj in model.objects.exclude(**{field.name: ''}).only('pk', field.name).iterator():
                    yield getattr(obj, field.name)
