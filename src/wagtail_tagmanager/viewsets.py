from django.apps import apps
from django.db.models import Count, F, IntegerField, OuterRef, Q, Subquery
from django.db.models.functions import Coalesce
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from wagtail_tagmanager.models import ManagedTag
from wagtail_tagmanager.panels import TagActionsPanel
from wagtail_tagmanager.utils import get_page_tagging_model


class ManagedTagViewSet(SnippetViewSet):
    model = ManagedTag
    icon = "tag"
    add_to_admin_menu = True
    menu_label = "Tags"
    menu_order = 500
    list_display = ["name", "slug", "object_count_number"]
    search_fields = ("name",)
    ordering = ["-object_count_number"]

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        TagActionsPanel(),
    ]

    # This query is used for the count of objects. It checks the list of
    # existing models against the models of the tags and filters out any models
    # that are not current. This avoids tags being counted for models that have been
    # deleted but their tag remains.
    # This query also combines the count of tags from the page model into the same count
    def get_queryset(self, request):
        page_tag_model = get_page_tagging_model()

        # Count the custom page tags
        page_tag_subquery = (
            page_tag_model.objects.filter(tag=OuterRef("pk"))
            .values("tag")
            .annotate(count=Count("id"))
            .values("count")
        )

        # Count the generic TaggedItems (with valid models)
        valid_models = [
            model.__name__.lower()
            for app_config in apps.get_app_configs()
            for model in app_config.get_models()
        ]

        return self.model.objects.annotate(
            page_tag_count=Subquery(page_tag_subquery, output_field=IntegerField()),
            tagged_item_count=Count(
                "taggit_taggeditem_items",
                filter=Q(taggit_taggeditem_items__content_type__model__in=valid_models),
                distinct=True,
            ),
        ).annotate(
            object_count_number=Coalesce(F("page_tag_count"), 0)
            + F("tagged_item_count")
        )


register_snippet(ManagedTagViewSet)
