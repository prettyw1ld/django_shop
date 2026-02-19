import django.core.validators
import django.db.models

import catalog.validators
from core.models import PublishedBaseModel


class Tag(PublishedBaseModel):
    name = django.db.models.CharField(
        max_length=150,
        verbose_name="название",
        help_text="max 150 символов",
    )
    slug = django.db.models.CharField(
        max_length=200,
        unique=True,
        verbose_name="слаг",
        validators=[catalog.validators.validate_slug],
    )

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"

    def __str__(self):
        return self.name


class Category(PublishedBaseModel):
    name = django.db.models.CharField(
        max_length=150,
        verbose_name="название",
        help_text="max 150 символов",
    )
    slug = django.db.models.CharField(
        max_length=200,
        unique=True,
        verbose_name="слаг",
        validators=[catalog.validators.validate_slug],
    )
    weight = django.db.models.IntegerField(
        default=100,
        validators=[
            django.core.validators.MinValueValidator(1),
            django.core.validators.MaxValueValidator(32767),
        ],
        verbose_name="вес",
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name


class Item(PublishedBaseModel):
    name = django.db.models.CharField(
        max_length=150,
        verbose_name="название",
        help_text="max 150 символов",
        unique=True,
    )
    text = django.db.models.TextField(
        verbose_name="текст",
        validators=[catalog.validators.validate_brilliant],
        help_text="Описание должно быть больше, чем из 2х слов и содержать"
        + ' слова "превосходно, роскошно" ',
    )
    tags = django.db.models.ManyToManyField(
        Tag,
        verbose_name="теги",
        help_text="Выберите теги",
    )
    category = django.db.models.ForeignKey(
        Category,
        on_delete=django.db.models.CASCADE,
        verbose_name="категории",
        help_text="Выберите категорию",
    )

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.name[:15]
