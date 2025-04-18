from django.contrib.auth import get_user_model
from django.contrib.messages.api import get_messages
from django.test import TestCase
from django.urls import reverse
from taggit.models import TaggedItem
from wagtail_factories import DocumentFactory

from tests.factories import HomePageFactory, ManagedTagFactory, TaggedItemFactory
from wagtail_tagmanager.models import ManagedTag
from wagtail_tagmanager.utils import get_page_tagging_model


class ManageTaggedObjectsViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="admin",
            password="pass",  # noqa: S106
            email="admin@example.com",
        )
        self.client.force_login(self.user)
        self.page_tag_model = get_page_tagging_model()

        self.tag = ManagedTagFactory()
        self.page = HomePageFactory(title="Home Page")
        self.page_tag = self.page_tag_model.objects.create(
            tag=self.tag, content_object=self.page
        )

    def test_get_view_lists_tagged_objects(self):
        url = reverse("wagtail_tagmanager_manage_objects", args=[self.tag.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Home Page")

    def test_search_filters_results(self):
        url = reverse("wagtail_tagmanager_manage_objects", args=[self.tag.pk])
        response = self.client.get(url, {"q": "something else"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Magic Page")

    def test_post_removes_tag_from_page_and_other_object(self):
        document = DocumentFactory(id=66)
        tagged_item = TaggedItemFactory(tag=self.tag, content_object=document)

        # Confirm they exist before deletion
        self.assertTrue(
            get_page_tagging_model()
            .objects.filter(tag=self.tag, content_object=self.page)
            .exists()
        )
        self.assertTrue(TaggedItem.objects.filter(id=tagged_item.id).exists())

        url = reverse("wagtail_tagmanager_manage_objects", args=[self.tag.pk])
        response = self.client.post(
            url,
            {
                "action": "remove_tag",
                "selected_items": [self.page.pk, document.pk],
            },
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            get_page_tagging_model()
            .objects.filter(tag=self.tag, content_object=self.page)
            .exists()
        )
        self.assertFalse(TaggedItem.objects.filter(id=tagged_item.id).exists())

    def test_success_message_after_removal(self):
        url = reverse("wagtail_tagmanager_manage_objects", args=[self.tag.pk])
        response = self.client.post(
            url,
            {
                "action": "remove_tag",
                "selected_items": [self.page.pk],
            },
            follow=True,
        )

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Removed tag" in message.message for message in messages))


class AddPagesToTagViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="admin",
            password="pass",  # noqa: S106
            email="admin@example.com",
        )
        self.client.force_login(self.user)
        self.page_tag_model = get_page_tagging_model()

        self.tag = ManagedTag.objects.create(name="Test Tag")
        self.page = HomePageFactory(title="Home Page")
        self.other_page = HomePageFactory(title="Another Page")

        self.page_tag_model.objects.create(tag=self.tag, content_object=self.page)

    def test_view_excludes_already_tagged_pages(self):
        url = reverse("wagtail_tagmanager_add_pages", args=[self.tag.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn("Another Page", content)
        self.assertNotIn("Home Page", content)

    def test_search_filters_results(self):
        url = reverse("wagtail_tagmanager_add_pages", args=[self.tag.pk])
        response = self.client.get(url, {"q": "another"})

        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn("Another Page", content)
        self.assertNotIn("Home Page", content)

    def test_post_adds_tag_to_selected_pages(self):
        url = reverse("wagtail_tagmanager_add_pages", args=[self.tag.pk])
        response = self.client.post(
            url,
            {
                "selected_items": [self.other_page.pk],
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            self.page_tag_model.objects.filter(
                tag=self.tag, content_object=self.other_page
            ).exists()
        )

    def test_success_message_after_adding_tag(self):
        url = reverse("wagtail_tagmanager_add_pages", args=[self.tag.pk])
        response = self.client.post(
            url,
            {
                "selected_items": [self.other_page.pk],
            },
            follow=True,
        )

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("added to" in message.message for message in messages))
