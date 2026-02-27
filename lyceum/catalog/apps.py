from django.apps import AppConfig

__all__ = []


class CatalogConfig(AppConfig):
    name = "catalog"
    verbose_name = "Каталог"
    default_auto_field = "django.db.models.BigAutoField"
