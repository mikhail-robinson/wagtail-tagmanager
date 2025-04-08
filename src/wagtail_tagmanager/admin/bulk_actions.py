

from wagtail.snippets.bulk_actions.snippet_bulk_action import SnippetBulkAction
from wagtail import hooks
from taggit.models import TaggedItem
from wagtail_tagmanager.models import ManagedTag
from wagtail_tagmanager.forms import MergeTagsForm
from wagtail_tagmanager.utils import get_page_tagging_model
from django.utils.translation import gettext_lazy as _

@hooks.register("register_bulk_action")
class MergeTagsBulkAction(SnippetBulkAction):
    display_name = _("Merge")
    aria_label = _("Merge selected tags")
    action_type = "merge_tags"
    template_name = "wagtail_tagmanager//templates/confirm_merge_tags.html"
    form_class = MergeTagsForm
    models = [ManagedTag]

    def get_execution_context(self):
        data = super().get_execution_context()
        data["form"] = self.cleaned_form
        return data

    @classmethod
    def execute_action(cls, objects, **kwargs):
        page_tag_model = get_page_tagging_model()
        new_name = kwargs["form"].cleaned_data["new_tag_name"]
        new_tag, _ = ManagedTag.objects.get_or_create(name=new_name)

        page_tag_model.objects.filter(tag__in=objects).update(tag=new_tag)
        TaggedItem.objects.filter(tag__in=objects).update(tag=new_tag)

        for tag in objects:
            if tag != new_tag:
                tag.delete()

        return len(objects), 0

    def get_success_message(self, num_parent_objects, num_child_objects):
        return _("{} tags have been merged.").format(num_parent_objects)