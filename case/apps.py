from django.apps import AppConfig


class CaseConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "case"

    def ready(self):
        import case.signals
