from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.admin.panels import FieldPanel
from django.db.models import Count
from wagtail_tagmanager.models import ManagedTag
from wagtail_tagmanager.panels import TagActionsPanel

class ManagedTagViewSet(SnippetViewSet):
    model = ManagedTag
    icon = "tag"
    add_to_admin_menu = True
    menu_label = "Tags"
    menu_order = 500
    list_display = ["name", "slug", "get_tagged_object_count"]
    search_fields = ("name",)
    ordering = ["-object_count_number"]

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        TagActionsPanel(),
    ]

    def get_queryset(self, request):
        return self.model.objects.annotate(
            object_count_number=Count("taggit_taggeditem_items", distinct=True)
        )
