import django.contrib.admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail

import catalog.models

__all__ = []


class MainImageInline(django.contrib.admin.StackedInline):
    model = catalog.models.MainImage
    extra = 1
    fields = ["image_tmb", "image"]
    readonly_fields = ["image_tmb"]

    def image_tmb(self, obj):
        if obj.pk and obj.image:
            return mark_safe(obj.image_tmb())
        elif obj.image:
            return mark_safe("Файл выбран (сохраните для просмотра)")
        return mark_safe("Нет изображения")

    image_tmb.short_description = "Превью"


class GalleryImageInline(django.contrib.admin.TabularInline):
    model = catalog.models.Images
    extra = 3
    fields = ["image_tmb", "image"]
    readonly_fields = ["image_tmb"]

    def image_tmb(self, obj):
        if obj.pk and obj.image:
            return mark_safe(obj.image_tmb())
        elif obj.image:
            return mark_safe("Файл выбран (сохраните для просмотра)")
        return mark_safe("Нет изображения")

    image_tmb.short_description = "Превью"


@django.contrib.admin.register(catalog.models.Category)
class CategoryAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        catalog.models.Category.name.field.name,
        catalog.models.Category.is_published.field.name,
    )


@django.contrib.admin.register(catalog.models.Tag)
class TagAdmin(django.contrib.admin.ModelAdmin):

    @django.contrib.admin.display(
        ordering=catalog.models.Tag.name.field.name,
    )
    def name(self, obj):
        return obj.name


@django.contrib.admin.register(catalog.models.Item)
class ItemAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
        "show_main_image",
        "gallery_images_count",
    )
    list_editable = (catalog.models.Item.is_published.field.name,)
    list_display_links = (catalog.models.Item.name.field.name,)
    filter_horizontal = (catalog.models.Item.tags.field.name,)
    inlines = [MainImageInline, GalleryImageInline]
    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    catalog.models.Item.name.field.name,
                    catalog.models.Item.is_published.field.name,
                    catalog.models.Item.category.field.name,
                    catalog.models.Item.tags.field.name,
                ),
            },
        ),
        (
            "Описание",
            {
                "fields": (catalog.models.Item.text.field.name,),
                "description": "Описание должно содержать слова "
                '"превосходно" и "роскошно"',
            },
        ),
    )

    def show_main_image(self, obj):
        if hasattr(obj, "main_image") and obj.main_image.image:
            thumbnail = get_thumbnail(
                obj.main_image.image, "50x50", crop="center", quality=90
            )
            return format_html(
                "<img src='{}' width='25' height='25' "
                "style='object-fit: cover; border-radius: 4px;' />",
                thumbnail.url,
            )
        return mark_safe("Нет фото")

    show_main_image.short_description = "Главное фото"

    def gallery_images_count(self, obj):
        count = obj.gallery_images.count()
        return f"{count} фото" if count else "Нет фото"

    gallery_images_count.short_description = "Галерея"

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .prefetch_related("gallery_images", "main_image")
        )


@django.contrib.admin.register(catalog.models.MainImage)
class MainImageAdmin(django.contrib.admin.ModelAdmin):
    list_display = [catalog.models.MainImage.item.field.name, "image_tmb"]
    readonly_fields = ["image_tmb"]

    def image_tmb(self, obj):
        return mark_safe(obj.image_tmb())

    image_tmb.short_description = "Превью"


@django.contrib.admin.register(catalog.models.Images)
class ImagesAdmin(django.contrib.admin.ModelAdmin):
    list_display = [
        catalog.models.Images.item.field.name,
        "image_tmb",
        catalog.models.Images.id.field.name,
    ]
    list_display_links = [catalog.models.Images.item.field.name]
    readonly_fields = ["image_tmb"]

    def image_tmb(self, obj):
        return mark_safe(obj.image_tmb())

    image_tmb.short_description = "Превью"
