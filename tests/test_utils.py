from django.apps import apps
from django.test import TestCase, override_settings
from wagtail.models import ImproperlyConfigured

from wagtail_tagmanager.utils import get_page_tagging_model


class GetPageTaggingModelTests(TestCase):
    @override_settings(WAGTAIL_TAGMANAGER_PAGE_TAG_MODEL="testapp.TestPageTag")
    def test_returns_correct_model_when_valid(self):
        model = get_page_tagging_model()
        self.assertEqual(model, apps.get_model("testapp", "TestPageTag"))

    @override_settings(WAGTAIL_TAGMANAGER_PAGE_TAG_MODEL=None)
    def test_raises_if_setting_missing(self):
        with self.assertRaisesMessage(
            ImproperlyConfigured,
            "WAGTAIL_TAGMANAGER_PAGE_TAG_MODEL setting must be defined to use wagtail-tagmanager.",
        ):
            get_page_tagging_model()

    @override_settings(WAGTAIL_TAGMANAGER_PAGE_TAG_MODEL="invalid.ModelPath")
    def test_raises_if_model_path_invalid(self):
        with self.assertRaisesMessage(
            ImproperlyConfigured,
            "WAGTAIL_TAGMANAGER_PAGE_TAG_MODEL refers to an invalid model: 'invalid.ModelPath'",
        ):
            get_page_tagging_model()

    @override_settings(WAGTAIL_TAGMANAGER_PAGE_TAG_MODEL="testapp.InvalidTagModel")
    def test_raises_if_model_not_subclass_of_taggeditembase(self):
        with self.assertRaisesMessage(
            ImproperlyConfigured,
            "WAGTAIL_TAGMANAGER_PAGE_TAG_MODEL must inherit from taggit.models.TaggedItemBase",
        ):
            get_page_tagging_model()
