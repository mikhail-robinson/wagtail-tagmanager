from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from taggit.models import TaggedItemBase


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
