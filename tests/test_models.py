from django.test import TestCase
from taggit.models import ContentType, TaggedItem
from wagtail_factories import DocumentFactory, ImageFactory

from tests.factories import (
    ManagedTagFactory,
    PageFactory,
    TaggedItemFactory,
)
from wagtail_tagmanager.models import ManagedTag
from wagtail_tagmanager.utils import get_page_tagging_model
from wagtail_tagmanager.viewsets import ManagedTagViewSet


class ManagedTagTestCase(TestCase):
    def setUp(self):
        self.page_tag_model = get_page_tagging_model()

    def test_managed_tag__returns_correct_get_tagged_object_count_number(self):
        tag = ManagedTagFactory()
        page1 = PageFactory()
        page2 = PageFactory()
        document = DocumentFactory(id=66)
        image = ImageFactory(id=702)

        self.page_tag_model.objects.create(tag=tag, content_object=page1)
        self.page_tag_model.objects.create(tag=tag, content_object=page2)

        ContentType.objects.create(app_label="fake_app", model="missingmodel")

        # Should not be included in count
        tagged_item_with_no_model_class = TaggedItem.objects.create(
            tag=tag,
            content_type=ContentType.objects.get(
                app_label="fake_app", model="missingmodel"
            ),
            object_id=12345,
        )
        self.assertIsNone(tagged_item_with_no_model_class.content_type.model_class())

        TaggedItemFactory(tag=tag, content_object=document)
        TaggedItemFactory(tag=tag, content_object=image)

        qs = ManagedTagViewSet().get_queryset(request=None)  # Mock or real request
        managed_tag = qs.get(pk=tag.pk)

        self.assertEqual(managed_tag.object_count_number, 4)

    def test_managed_tag__returns_correct_list_of_tagged_objects(self):
        tag = ManagedTagFactory()
        page = PageFactory()
        document = DocumentFactory(id=707)
        image = ImageFactory(id=66)

        self.page_tag_model.objects.create(tag=tag, content_object=page)
        TaggedItemFactory(tag=tag, content_object=document)
        TaggedItemFactory(tag=tag, content_object=image)

        ContentType.objects.create(app_label="fake_app", model="missingmodel")

        # if a model is deleted, the model_class in the TaggedItem model is set to None
        # which can impact how tagged objects results are collected.
        tagged_item_with_no_model_class = TaggedItem.objects.create(
            tag=tag,
            content_type=ContentType.objects.get(
                app_label="fake_app", model="missingmodel"
            ),
            object_id=12345,
        )
        self.assertIsNone(tagged_item_with_no_model_class.content_type.model_class())

        managed_tag = ManagedTag.objects.get(pk=tag.pk)

        result = managed_tag.get_tagged_objects()
        expected_objects = [page, document, image]
        self.assertEqual(result, expected_objects)
