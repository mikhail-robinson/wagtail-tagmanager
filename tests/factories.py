import io

import wagtail_factories
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile
from factory import LazyAttribute, LazyFunction, Sequence, SubFactory, lazy_attribute
from factory.django import DjangoModelFactory
from PIL import Image as PilImage
from taggit.models import Tag, TaggedItem
from wagtail.models import Page


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    name = Sequence(lambda n: f"Tag {n}")


class PageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = Page

    parent = None
    title = Sequence(lambda n: f"Test Page {n}")
    slug = Sequence(lambda n: f"test-page-{n}")


class TaggedItemFactory(DjangoModelFactory):
    class Meta:
        model = TaggedItem

    tag = SubFactory(TagFactory)
    content_object = SubFactory(wagtail_factories.DocumentFactory)

    @lazy_attribute
    def content_type(self):
        return ContentType.objects.get_for_model(self.content_object.__class__)

    @lazy_attribute
    def object_id(self):
        return self.content_object.pk


class HomePageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = Page

    parent = None
    title = "Home Page"
    slug = "home-page"


class CustomDocumentFactory(wagtail_factories.DocumentFactory):
    file = LazyAttribute(lambda _: ContentFile(b"Fake file content", "test.txt"))


def simple_image():
    buffer = io.BytesIO()
    PilImage.new("RGB", (10, 10)).save(buffer, format="JPEG")
    return ContentFile(buffer.getvalue(), "image.jpg")


class CustomImageFactory(wagtail_factories.ImageFactory):
    file = LazyFunction(simple_image)
