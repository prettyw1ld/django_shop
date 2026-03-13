__all__ = ("Item", "Tag", "Category", "Image", "MainImage")

import django.contrib.admin
import django.core.validators
import django.db.models
from django.utils.safestring import mark_safe
from django_ckeditor_5.fields import CKEditor5Field

from catalog.managers import ItemsManager
from catalog.validators import WordsValidator
from core.managers import (
    PublishedManager,
)
from core.models import (
    ImageBaseModel,
    NormalizedNameMixin,
    PublishedBaseModel,
)


class Tag(PublishedBaseModel, NormalizedNameMixin):
    objects = PublishedManager()
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
    objects = PublishedManager()
    slug = django.db.models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="слаг",
        help_text="Максимум 200 символов",
    )
    weight = django.db.models.PositiveSmallIntegerField(
        default=100,
        validators=[
            django.core.validators.MinValueValidator(1),
            django.core.validators.MaxValueValidator(32767),
        ],
        verbose_name="вес",
        help_text="Максимум 32767",
    )

    class Meta:
        ordering = ("weight", "id")
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Item(PublishedBaseModel):
    text = CKEditor5Field(
        verbose_name="описание",
        help_text="Описание должно быть больше, чем из 2х слов и "
        " содержать слова: превосходно, роскошно",
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

    updated = django.db.models.DateTimeField(
        verbose_name="время изменения",
        auto_now=True,
        null=True,
    )

    created = django.db.models.DateTimeField(
        verbose_name="время создания",
        auto_now_add=True,
        null=True,
    )

    objects = ItemsManager()

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"
        default_related_name = "items"

    @django.contrib.admin.display(description="Изображение")
    def image_tmb(self):
        if hasattr(self, "main_image") and self.main_image.image:
            tmb = self.main_image.get_image_50x50()
            if tmb:
                return mark_safe(f'<img src="{tmb.url}">')

        return "Нет изображения"


class MainImage(ImageBaseModel):
    item = django.db.models.OneToOneField(
        Item,
        on_delete=django.db.models.CASCADE,
        related_name="main_image",
        verbose_name="главное изображение",
    )

    class Meta:
        verbose_name = "главное изображение"
        verbose_name_plural = "главные изображения"

    def __str__(self):
        return self.item.name


class Image(ImageBaseModel):
    item = django.db.models.ForeignKey(
        Item,
        on_delete=django.db.models.CASCADE,
        related_name="images",
        verbose_name="изображения",
    )

    class Meta:
        verbose_name = "фото"
        verbose_name_plural = "фото"
