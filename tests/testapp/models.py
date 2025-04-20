from django.db import models
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.models import Page


class TestPageTag(TaggedItemBase):
    content_object = ParentalKey(Page, on_delete=models.CASCADE)


class TestCustomPage(Page):
    def __str__(self):
        return self.title


class CustomPageTag(TaggedItemBase):
    content_object = ParentalKey(TestCustomPage, on_delete=models.CASCADE)


class InvalidTagModel(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
