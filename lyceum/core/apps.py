from django.apps import AppConfig

__all__ = []


class CoreConfig(AppConfig):
    name = "core"
    verbose_name = "Базовые сущности"
    default_auto_field = "django.db.models.BigAutoField"
