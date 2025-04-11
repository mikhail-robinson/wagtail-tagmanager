from django.apps import apps
from django.db.models import Count, Q
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from wagtail_tagmanager.models import ManagedTag
from wagtail_tagmanager.panels import TagActionsPanel


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

    def get_queryset(self, request):
        # Get all valid model names
        valid_models = []
        for app_config in apps.get_app_configs():
            for model in app_config.get_models():
                valid_models.append(model.__name__.lower())

        return self.model.objects.annotate(
            object_count_number=Count(
                "taggit_taggeditem_items",
                filter=Q(taggit_taggeditem_items__content_type__model__in=valid_models),
                distinct=True,
            )
        )


register_snippet(ManagedTagViewSet)
