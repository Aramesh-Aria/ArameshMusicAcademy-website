import os
import time

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.core.image_utils import SIZES_DIR, _is_size_copy
from apps.core.media_cleanup import file_fields, models_with_files

RECENT_SECONDS = 60 * 60


class Command(BaseCommand):
    help = (
        'List the files in MEDIA_ROOT that no row names any more: photos that were replaced or whose row was '
        'deleted before the site removed them itself, and the srcset copies of such photos. It looks only in the '
        'folders uploads go to. Lists only; pass '
        '--delete to remove them. Files changed in the last hour are left alone (an upload may be in progress).'
    )

    def add_arguments(self, parser):
        parser.add_argument('--delete', action='store_true', help='Remove the listed files. Cannot be undone.')

    def handle(self, *args, **options):
        root = settings.MEDIA_ROOT
        referenced = self.referenced_names()
        orphans, skipped_recent, elsewhere = self.orphans(root, referenced)
        total = sum(size for _, size in orphans)

        for name, size in orphans:
            self.stdout.write(f'{name}  ({size / 1024:.0f} KB)')
        summary = (
            f'{len(orphans)} unused files, {total / 1024 / 1024:.1f} MB; '
            f'{len(referenced)} files are in use and stay.'
        )
        if skipped_recent:
            summary += f' {skipped_recent} unused files changed in the last hour were left out.'
        if elsewhere:
            summary += f' {elsewhere} files outside the upload folders were not looked at.'

        if not options['delete']:
            self.stdout.write(self.style.SUCCESS(f'{summary} Nothing was removed; run again with --delete to remove them.'))
            return
        if orphans and not referenced:
            # An empty or wrong database (DATABASE_PATH) would make every upload look unused.
            raise CommandError('The database names no uploaded file at all, so nothing was removed. Is this the right database?')
        for name, _ in orphans:
            os.remove(os.path.join(root, name))
        self.remove_empty_folders(root)
        self.stdout.write(self.style.SUCCESS(f'{summary} Removed.'))

    def referenced_names(self):
        names = set()
        for model in models_with_files():
            for field in file_fields(model):
                names.update(
                    model._base_manager.exclude(**{field.name: ''}).values_list(field.name, flat=True).distinct()
                )
        names.discard(None)
        return names

    def upload_folders(self):
        """The folders this site's own uploads and their copies go to. Nothing outside them is ever touched."""
        folders = {f'{SIZES_DIR}/'}
        for model in models_with_files():
            for field in file_fields(model):
                if isinstance(field.upload_to, str) and field.upload_to.strip('/'):
                    folders.add(field.upload_to.strip('/') + '/')
        return tuple(folders)

    def orphans(self, root, referenced):
        now = time.time()
        folders = self.upload_folders()
        found, skipped_recent, elsewhere = [], 0, 0
        for folder, _, files in os.walk(root):
            for entry in files:
                path = os.path.join(folder, entry)
                name = os.path.relpath(path, root).replace(os.sep, '/')
                if entry.startswith('.'):
                    continue
                if not name.startswith(folders):
                    elsewhere += 1
                    continue
                if self.is_in_use(name, referenced):
                    continue
                if now - os.path.getmtime(path) < RECENT_SECONDS:
                    skipped_recent += 1
                    continue
                found.append((name, os.path.getsize(path)))
        return sorted(found), skipped_recent, elsewhere

    def is_in_use(self, name, referenced):
        if not name.startswith(f'{SIZES_DIR}/'):
            return name in referenced
        # A copy stays while the photo it was made from is in use.
        stem = name[len(SIZES_DIR) + 1:].rsplit('-', 1)[0]
        return any(
            _is_size_copy(name, original)
            for original in referenced if os.path.splitext(original)[0] == stem
        )

    def remove_empty_folders(self, root):
        for folder, _, _ in os.walk(root, topdown=False):
            if folder != root and not os.listdir(folder):
                os.rmdir(folder)
