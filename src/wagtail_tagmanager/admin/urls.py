from django.urls import path
from wagtail import hooks

from wagtail_tagmanager.views import AddPagesToTagView, ManageTaggedObjectsView


@hooks.register("register_admin_urls")
def register_managed_tagged_object_admin_urls():
    return [
        path(
            "tags/<int:tag_id>/objects/",
            ManageTaggedObjectsView.as_view(),
            name="wagtail_tagmanager_manage_objects",
        ),
        path(
            "tags/<int:tag_id>/add-pages/",
            AddPagesToTagView.as_view(),
            name="wagtail_tagmanager_add_pages",
        ),
    ]
