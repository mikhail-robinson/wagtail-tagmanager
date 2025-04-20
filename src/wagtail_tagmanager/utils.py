import logging

from django.apps import apps
from django.conf import settings
from django.core.exceptions import FieldDoesNotExist, ImproperlyConfigured
from taggit.models import TaggedItemBase
from wagtail.models import Page


def get_page_tagging_model():
    """
    Returns the model used to store tag-to-page relationships.
    Users must define this via the WAGTAIL_TAGMANAGER_PAGE_TAG_MODEL setting.
    """
    model_path = getattr(settings, "WAGTAIL_TAGMANAGER_PAGE_TAG_MODEL", None)

    if not model_path:
        raise ImproperlyConfigured(
            "WAGTAIL_TAGMANAGER_PAGE_TAG_MODEL setting must be defined to use wagtail-tagmanager."
        )

    try:
        model = apps.get_model(model_path)
    except (ValueError, LookupError) as err:
        raise ImproperlyConfigured(
            f"WAGTAIL_TAGMANAGER_PAGE_TAG_MODEL refers to an invalid model: '{model_path}'"
        ) from err

    if not issubclass(model, TaggedItemBase):
        raise ImproperlyConfigured(
            "WAGTAIL_TAGMANAGER_PAGE_TAG_MODEL must inherit from taggit.models.TaggedItemBase"
        )

    return model


def get_base_page_model():  # noqa: C901
    model_path = getattr(settings, "WAGTAIL_TAGMANAGER_BASE_PAGE_MODEL", None)

    if model_path:
        try:
            return apps.get_model(model_path)
        except (ValueError, LookupError) as err:
            raise ImproperlyConfigured(
                f"WAGTAIL_TAGMANAGER_BASE_PAGE_MODEL refers to an invalid model: '{model_path}'"
            ) from err

    valid_models = []
    for model in apps.get_models():
        if issubclass(model, TaggedItemBase):
            try:
                content_object_field = model._meta.get_field("content_object")
                related_model = getattr(content_object_field, "related_model", None)

                if related_model and issubclass(related_model, Page):
                    valid_models.append(related_model)

            except FieldDoesNotExist:
                logging.warning(
                    f"TaggedItemBase model '{model.__name__}' is missing a 'content_object' field."
                )

            except Exception as err:
                logging.exception(
                    f"Error inspecting related model for '{model.__name__}': {err}"
                )

    if len(valid_models) > 1:
        logging.warning(
            f"Multiple valid base page models found: {valid_models}. "
            "The first one found will be used. Consider specifying WAGTAIL_TAGMANAGER_BASE_PAGE_MODEL "
            "to avoid ambiguity."
        )

    if not valid_models:
        raise ImproperlyConfigured(
            "Could not determine base page model automatically. "
            "Please define WAGTAIL_TAGMANAGER_BASE_PAGE_MODEL in settings."
        )

    return valid_models[0]  # Return the first valid model found
