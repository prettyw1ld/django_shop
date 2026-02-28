import django.contrib.admin

import catalog.models

__all__ = []

django.contrib.admin.site.register(catalog.models.Category)
django.contrib.admin.site.register(catalog.models.Tag)


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
    )
    catalog.models.Item.image_tmb.short_description = "фото"
    list_editable = (catalog.models.Item.is_published.field.name,)
    list_display_links = (catalog.models.Item.name.field.name,)
    filter_horizontal = (catalog.models.Item.tags.field.name,)
    inlines = [MainImage, Image]
