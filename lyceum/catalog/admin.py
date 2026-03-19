__all__ = ()

import django.contrib.admin

import catalog.models


@django.contrib.admin.register(catalog.models.Category)
class CategoryAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        catalog.models.Category.name.field.name,
        catalog.models.Category.weight.field.name,
        catalog.models.Category.canonical_name.field.name,
    )
    list_display_links = (catalog.models.Category.name.field.name,)


@django.contrib.admin.register(catalog.models.Tag)
class TagAdmin(django.contrib.admin.ModelAdmin):
    list_display = (catalog.models.Tag.name.field.name,)
    list_display_links = (catalog.models.Tag.name.field.name,)


class MainImage(django.contrib.admin.TabularInline):
    model = catalog.models.MainImage
    fields = ("image",)


class Image(django.contrib.admin.TabularInline):
    model = catalog.models.Image
    fields = ("image",)


@django.contrib.admin.register(catalog.models.Item)
class ItemAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
        catalog.models.Item.image_tmb,
        catalog.models.Item.created.field.name,
        catalog.models.Item.updated.field.name,
    )
    list_editable = (catalog.models.Item.is_published.field.name,)
    list_display_links = (catalog.models.Item.name.field.name,)
    filter_horizontal = (catalog.models.Item.tags.field.name,)
    inlines = (MainImage, Image)
    readonly_fields = (
        catalog.models.Item.created.field.name,
        catalog.models.Item.updated.field.name,
    )
