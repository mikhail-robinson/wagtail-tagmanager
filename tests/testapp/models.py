from django.db import models
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.models import Page


class TestPageTag(TaggedItemBase):
    content_object = ParentalKey(
        Page, related_name="test_tagged_items", on_delete=models.CASCADE
    )
