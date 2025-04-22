from django.db.models import IntegerField
from django.db.models.expressions import RawSQL
from taggit.models import TaggedItem
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
    def get_queryset(self, request):  # noqa S608, S611
        page_tag_model = get_page_tagging_model()
        page_tag_table = page_tag_model._meta.db_table
        tagged_item_table = TaggedItem._meta.db_table
        tag_table = self.model._meta.db_table

        object_count_sql = f"""
            SELECT COUNT(DISTINCT object_key) FROM (
                SELECT CONCAT('page-', content_object_id) AS object_key
                FROM {page_tag_table}
                WHERE tag_id = {tag_table}.id

                UNION ALL

                SELECT CONCAT(content_type_id, '-', object_id) AS object_key
                FROM {tagged_item_table}
                WHERE tag_id = {tag_table}.id
            ) AS combined
        """  # noqa S608

        return self.model.objects.annotate(
            object_count_number=RawSQL(  # noqa S611
                object_count_sql, [], output_field=IntegerField()
            )
        )


register_snippet(ManagedTagViewSet)
