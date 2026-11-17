"""
Uploads that no row names any more are removed from disk.

Django never deletes a file itself: replacing a teacher's portrait, clearing a Programme's photo or deleting a
gallery image left the old file (and its srcset copies) in MEDIA_ROOT for good. These handlers remove it once the
change has committed, and only when no row of any model still names that file. `manage.py clean_media` removes
what was left behind before these handlers existed.
"""
import logging

from django.apps import apps
from django.db import models, transaction
from django.db.models.signals import post_delete, post_save, pre_save

from .image_utils import delete_image

logger = logging.getLogger(__name__)


def file_fields(model):
    return [field for field in model._meta.concrete_fields if isinstance(field, models.FileField)]


def models_with_files():
    return [model for model in apps.get_models() if file_fields(model)]


def is_referenced(name):
    """Whether any row of any model names this stored file."""
    return any(
        model._base_manager.filter(**{field.name: name}).exists()
        for model in models_with_files() for field in file_fields(model)
    )


def _delete_if_unused(storage, name):
    try:
        if not is_referenced(name):
            delete_image(storage, name)
    except Exception:  # a file left on disk must never fail the save that replaced it
        logger.exception('Could not remove the replaced upload %s', name)


def _discard(storage, name):
    transaction.on_commit(lambda: _delete_if_unused(storage, name))


def _remember_stored_files(sender, instance, raw=False, **kwargs):
    fields = file_fields(sender)
    if not fields:
        return
    instance._stored_files = {}
    if raw or instance._state.adding or instance.pk is None:
        return
    row = sender._base_manager.filter(pk=instance.pk).values(*[field.name for field in fields]).first()
    instance._stored_files = row or {}


def _delete_replaced_files(sender, instance, **kwargs):
    for field in file_fields(sender):
        old_name = getattr(instance, '_stored_files', {}).get(field.name)
        if old_name and old_name != getattr(instance, field.name).name:
            _discard(field.storage, old_name)


def _delete_files_of_a_deleted_row(sender, instance, **kwargs):
    for field in file_fields(sender):
        name = getattr(instance, field.name).name
        if name:
            _discard(field.storage, name)


def connect():
    pre_save.connect(_remember_stored_files, dispatch_uid='media_cleanup.remember')
    post_save.connect(_delete_replaced_files, dispatch_uid='media_cleanup.replaced')
    post_delete.connect(_delete_files_of_a_deleted_row, dispatch_uid='media_cleanup.deleted')
