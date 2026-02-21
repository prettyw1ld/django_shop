import django.core.validators
import django.db.models

from catalog.validators import validate_slug, WordsValidator
from core.models import PublishedBaseModel


class Tag(PublishedBaseModel):
    slug = django.db.models.CharField(
        max_length=200,
        unique=True,
        verbose_name="слаг",
        validators=[validate_slug],
        help_text="слаг",
    )

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"
        default_related_name = "tags"

    def __str__(self):
        return self.name


class Category(PublishedBaseModel):
    slug = django.db.models.CharField(
        max_length=200,
        unique=True,
        verbose_name="слаг",
        validators=[validate_slug],
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
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name


class Item(PublishedBaseModel):
    text = django.db.models.TextField(
        verbose_name="описание",
        help_text="Описание должно быть больше, чем из 2х слов и содержать"
        + ' слова "превосходно, роскошно"',
        validators=[
            WordsValidator(
                "превосходно",
                "роскошно",
            )
        ],
    )
    tags = django.db.models.ManyToManyField(Tag)
    category = django.db.models.ForeignKey(
        Category,
        on_delete=django.db.models.CASCADE,
        verbose_name="категория",
        help_text="Выберите категорию",
    )

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"
        default_related_name = "items"

    def __str__(self):
        return self.name[:15]
