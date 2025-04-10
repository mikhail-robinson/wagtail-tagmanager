from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WagtailTagmanagerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "wagtail_tagmanager"
    label = "wagtail_tagmanager"
    verbose_name = _("Wagtail Tag Manager")

    def ready(self):
        import wagtail_tagmanager.bulk_actions  # noqa:F401
        import wagtail_tagmanager.urls  # noqa:F401
        import wagtail_tagmanager.viewsets  # noqa:F401
