from django.apps import apps
from django.test import TestCase, override_settings
from wagtail.models import ImproperlyConfigured, Page

from tests.testapp.models import InvalidTagModel
from wagtail_tagmanager.utils import get_base_page_model, get_page_tagging_model


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


class GetBasePageModelTests(TestCase):
    @override_settings(WAGTAIL_TAGMANAGER_BASE_PAGE_MODEL="testapp.TestCustomPage")
    def test_returns_model_from_setting(self):
        model = get_base_page_model()
        self.assertEqual(model, apps.get_model("testapp", "TestCustomPage"))

    @override_settings(WAGTAIL_TAGMANAGER_BASE_PAGE_MODEL="invalid.ModelPath")
    def test_raises_if_invalid_setting(self):
        with self.assertRaisesMessage(
            ImproperlyConfigured,
            "WAGTAIL_TAGMANAGER_BASE_PAGE_MODEL refers to an invalid model: 'invalid.ModelPath'",
        ):
            get_base_page_model()

    @override_settings(WAGTAIL_TAGMANAGER_BASE_PAGE_MODEL=None)
    def test_falls_back_to_page_if_tag_targets_page(self):
        # `TestPageTag` uses Page as its content_object
        model = get_base_page_model()
        self.assertEqual(model, Page)

    @override_settings(WAGTAIL_TAGMANAGER_BASE_PAGE_MODEL=None)
    def test_warns_if_multiple_valid_models_found(self):
        with self.assertLogs(level="WARNING") as cm:
            get_base_page_model()

        self.assertIn("Multiple valid base page models found", "\n".join(cm.output))

    @override_settings(WAGTAIL_TAGMANAGER_BASE_PAGE_MODEL=None)
    def test_raises_if_no_valid_tag_model_found(self):
        # Temporarily remove TaggedItemBase subclasses from the registry
        # (simulate a broken install)
        original_models = apps.get_models
        apps.get_models = lambda: [InvalidTagModel]

        with self.assertRaisesMessage(
            ImproperlyConfigured,
            "Could not determine base page model automatically. "
            "Please define WAGTAIL_TAGMANAGER_BASE_PAGE_MODEL in settings.",
        ):
            get_base_page_model()

        apps.get_models = original_models
