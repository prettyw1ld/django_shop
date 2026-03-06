__all__ = []

import django.core.validators
import django.db.models
from django.utils.safestring import mark_safe

# from django.utils.html import format_html
from django_ckeditor_5.fields import CKEditor5Field
from sorl.thumbnail import get_thumbnail

from catalog.validators import WordsValidator
from core.models import NormalizedNameMixin, PublishedBaseModel


def item_directory_path(instance, filename):
    return f"catalog/{instance.item.id}/{filename}"


class ImageBaseModel(django.db.models.Model):
    image = django.db.models.ImageField(
        "изображение",
        upload_to=item_directory_path,
        default=None,
    )

    def get_image_300x300(self):
        return get_thumbnail(
            self.image,
            "300x300",
            crop="center",
            quality=51,
        )

    def get_image_50x50(self):
        return get_thumbnail(
            self.image,
            "50x50",
            crop="center",
            quality=51,
        )

    class Meta:
        abstract = True


class Tag(PublishedBaseModel, NormalizedNameMixin):
    slug = django.db.models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="слаг",
        help_text="слаг",
    )

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"
        default_related_name = "tags"


class Category(PublishedBaseModel, NormalizedNameMixin):
    slug = django.db.models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="слаг",
        help_text="Максимум 200 символов",
    )
    weight = django.db.models.IntegerField(
        default=100,
        validators=[
            django.core.validators.MinValueValidator(1),
            django.core.validators.MaxValueValidator(32767),
        ],
        verbose_name="вес",
        help_text="Max 32767",
    )

    class Meta:
        ordering = ("weight", "id")
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Item(PublishedBaseModel):
    text = CKEditor5Field(
        verbose_name="описание",
        help_text="Описание должно быть больше, чем из 2х слов и "
        + " содержать слова: превосходно, роскошно",
        validators=[
            WordsValidator(
                "превосходно",
                "роскошно",
            ),
        ],
    )
    tags = django.db.models.ManyToManyField(Tag)
    category = django.db.models.ForeignKey(
        Category,
        on_delete=django.db.models.CASCADE,
        verbose_name="категория",
        help_text="Выберите категорию",
    )
    is_on_main = django.db.models.BooleanField(
        default=False,
        verbose_name="отображение на главной",
    )

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"
        default_related_name = "items"

    @django.contrib.admin.display(description="Фото")
    def image_tmb(self):
        if hasattr(self, "main_image") and self.main_image:
            thumbnail = get_thumbnail(
                self.main_image.image,
                "50x50",
                crop="center",
                quality=51,
            )
            return mark_safe(
                f'<img src="{thumbnail.url}" width="50" height="50" />',
            )
            # return format_html(
            #     '<img src="{}" width="50" height="50">',
            #     thumbnail.url,
            # )
        return "Нет фото"


class MainImage(ImageBaseModel):
    item = django.db.models.OneToOneField(
        Item,
        on_delete=django.db.models.CASCADE,
        related_name="main_image",
        verbose_name="Главное изображение",
    )

    def __str__(self):
        return self.item.name

    class Meta:
        verbose_name = "главное изображение"
        verbose_name_plural = "главные изображения"


class Image(ImageBaseModel):
    item = django.db.models.ForeignKey(
        Item,
        on_delete=django.db.models.CASCADE,
        related_name="images",
        verbose_name="Изображения",
    )

    class Meta:
        verbose_name = "фото"
        verbose_name_plural = "фото"
