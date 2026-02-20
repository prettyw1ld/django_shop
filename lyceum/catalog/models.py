import django.core.validators
import django.db.models

from catalog.validators import validate_slug, ValidateMustContain
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

    def __str__(self):
        return self.name


class Category(PublishedBaseModel):
    slug = django.db.models.CharField(
        max_length=200,
        unique=True,
        verbose_name="слаг",
        validators=[validate_slug],
        help_text="слаг",
    )
    weight = django.db.models.IntegerField(
        default=100,
        validators=[
            django.core.validators.MinValueValidator(1),
            django.core.validators.MaxValueValidator(32767),
        ],
        verbose_name="вес",
        help_text="вес",
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name


class Item(PublishedBaseModel):
    text = django.db.models.TextField(
        verbose_name="текст",
        validators=[ValidateMustContain("превосходно", "роскошно")],
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
        verbose_name="категория",
        help_text="Выберите категорию",
    )

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.name[:15]
