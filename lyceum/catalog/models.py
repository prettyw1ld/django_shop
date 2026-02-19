import django.core.validators
import django.db.models

import catalog.validators
from core.models import PublishedBaseModel


class Tag(PublishedBaseModel):
    name = django.db.models.CharField(max_length=150, verbose_name="Название")
    slug = django.db.models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Слаг",
        validators=[catalog.validators.validate_slug],
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Category(PublishedBaseModel):
    name = django.db.models.CharField(max_length=150, verbose_name="Название")
    slug = django.db.models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Слаг",
        validators=[catalog.validators.validate_slug],
    )
    weight = django.db.models.IntegerField(
        default=100,
        validators=[
            django.core.validators.MinValueValidator(1),
            django.core.validators.MaxValueValidator(32767),
        ],
        verbose_name="Вес",
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Item(PublishedBaseModel):
    name = django.db.models.CharField(
        max_length=150,
        verbose_name="Название",
        help_text="max 150 символов",
        unique=True,
    )
    text = django.db.models.TextField(
        verbose_name="Текст",
        validators=[catalog.validators.validate_brilliant],
        help_text="Описание должно быть больше, чем из 2х слов и содержать"
        + ' слова "превосходно, роскошно" ',
    )
    tags = django.db.models.ManyToManyField(
        Tag,
        verbose_name="Теги",
        help_text="Выберите теги",
    )
    category = django.db.models.ForeignKey(
        Category,
        on_delete=django.db.models.CASCADE,
        verbose_name="Категории",
        help_text="Выберите категорию",
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name[:15]
