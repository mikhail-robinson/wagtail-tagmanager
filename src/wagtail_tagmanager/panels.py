from django.urls import reverse
from django.utils.safestring import mark_safe
from wagtail.admin.panels import Panel


class TagActionsPanel(Panel):
    """
    Shows admin actions related to the tag, like managing pages.
    """

    def clone(self):
        return self.__class__()

    def get_bound_panel(self, instance=None, request=None, form=None, prefix="panel"):
        return self.BoundPanel(
            panel=self,
            instance=instance,
            request=request,
            form=form,
            prefix=prefix,
        )

    class BoundPanel(Panel.BoundPanel):
        def render_html(self, parent_context=None):
            if not self.instance.pk:
                return ""

            url = (
                reverse("wagtail_tagmanager_manage_objects", args=[self.instance.pk])
                + f"?tag_id={self.instance.pk}"
            )

            return mark_safe(f"""
                <div class="field-content">
                    <a href="{url}" class="button button-secondary">
                        View and remove tagged objects
                    </a>
                </div>
            """)
