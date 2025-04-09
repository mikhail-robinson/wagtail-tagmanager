from django.apps import AppConfig


class WagtailTagmanagerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "wagtail_tagmanager"

    def ready(self):
        import wagtail_tagmanager.admin.urls  # noqa: F401
