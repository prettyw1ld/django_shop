import django.contrib.admin

import catalog.models

category_name = catalog.models.Category.name.field.name
category_published = catalog.models.Category.is_published.field.name
tag_name = catalog.models.Tag.name.field.name
item_name = catalog.models.Item.name.field.name
item_published = catalog.models.Item.is_published.field.name
item_tags = catalog.models.Item.tags.field.name


@django.contrib.admin.register(catalog.models.Category)
class CategoryAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        category_name,
        category_published,
    )

    @django.contrib.admin.display(description="Название", ordering="name")
    def name(self, obj):
        return getattr(obj, category_name)

    @django.contrib.admin.display(
        description="Опубликовано",
        boolean=True,
        ordering="is_published",
    )
    def is_published(self, obj):
        return getattr(obj, category_published)


@django.contrib.admin.register(catalog.models.Tag)
class TagAdmin(django.contrib.admin.ModelAdmin):
    list_display = (tag_name,)

    @django.contrib.admin.display(description="Название", ordering="name")
    def name(self, obj):
        return getattr(obj, tag_name)


@django.contrib.admin.register(catalog.models.Item)
class ItemAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        item_name,
        item_published,
    )
    list_editable = (item_published,)
    list_display_links = (item_name,)
    filter_horizontal = (item_tags,)

    @django.contrib.admin.display(description="Название", ordering="name")
    def name(self, obj):
        return getattr(obj, item_tags)

    @django.contrib.admin.display(
        description="Опубликовано",
        boolean=True,
        ordering="is_published",
    )
    def is_published(self, obj):
        return getattr(obj, item_published)
