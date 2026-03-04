__all__ = []

from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "core"
    verbose_name = "Базовые сущности"
    default_auto_field = "django.db.models.BigAutoField"
