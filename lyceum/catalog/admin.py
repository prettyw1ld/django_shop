import django.contrib.admin

import catalog.models


@django.contrib.admin.register(catalog.models.Category)
class CategoryAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        catalog.models.Category.name.field.name,
        catalog.models.Category.is_published.field.name,
    )


@django.contrib.admin.register(catalog.models.Tag)
class TagAdmin(django.contrib.admin.ModelAdmin):
    list_display = (catalog.models.Tag.name.field.name,)


@django.contrib.admin.register(catalog.models.Item)
class ItemAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
    )
    list_editable = (catalog.models.Item.is_published.field.name,)
    list_display_links = (catalog.models.Item.name.field.name,)
    filter_horizontal = (catalog.models.Item.tags.field.name,)

    @django.contrib.admin.display(description="Название", ordering="name")
    def name(self, obj):
        return getattr(obj, catalog.models.Item.name.field.name)

    @django.contrib.admin.display(
        description="Опубликовано", boolean=True, ordering="is_published"
    )
    def is_published(self, obj):
        return getattr(obj, catalog.models.Item.is_published.field.name)
