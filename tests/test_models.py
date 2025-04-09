from django.test import TestCase
from wagtail_factories import DocumentFactory, ImageFactory

from tests.factories import (
    PageFactory,
    TagFactory,
    TaggedItemFactory,
)
from wagtail_tagmanager.models import ManagedTag
from wagtail_tagmanager.utils import get_page_tagging_model


class ManagedTagTestCase(TestCase):
    def setUp(self):
        self.page_tag_model = get_page_tagging_model()

    def test_managed_tag__returns_correct_get_tagged_object_count_number(self):
        tag = TagFactory()
        page1 = PageFactory()
        page2 = PageFactory()

        self.page_tag_model.objects.create(tag=tag, content_object=page1)
        self.page_tag_model.objects.create(tag=tag, content_object=page2)
        managed_tag = ManagedTag.objects.get(pk=tag.pk)

        self.assertEqual(managed_tag.get_tagged_object_count(), 2)

    def test_managed_tag__returns_correct_list_of_tagged_objects(self):
        tag = TagFactory()
        page = PageFactory()
        document = DocumentFactory()
        image = ImageFactory()

        self.page_tag_model.objects.create(tag=tag, content_object=page)
        TaggedItemFactory(tag=tag, content_object=document)
        TaggedItemFactory(tag=tag, content_object=image)

        managed_tag = ManagedTag.objects.get(pk=tag.pk)

        result = managed_tag.get_tagged_objects()

        expected_objects = [page, document, image]

        self.assertEqual(result, expected_objects)
