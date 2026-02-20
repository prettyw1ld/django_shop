import django.contrib.admin

import catalog.models


@django.contrib.admin.register(catalog.models.Category)
class CategoryAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        "name",
        "is_published",
    )


@django.contrib.admin.register(catalog.models.Tag)
class TagAdmin(django.contrib.admin.ModelAdmin):
    list_display = ("name",)


@django.contrib.admin.register(catalog.models.Item)
class ItemAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        "name",
        "is_published",
    )
    list_editable = ("is_published",)
    list_display_links = ("name",)
    filter_horizontal = ("tags",)

    @django.contrib.admin.display(
        description="Название",
        ordering="name",
    )
    def name(self, obj):
        return getattr(obj, "name")

    @django.contrib.admin.display(
        description="Опубликовано",
        boolean=True,
        ordering="is_published",
    )
    def is_published(self, obj):
        return getattr(obj, "is_published")
