from ckeditor.fields import RichTextField
import django.core.validators
import django.db.models
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail

from catalog.validators import WordsValidator
from core.models import NormalizedNameMixin, PublishedBaseModel

__all__ = ["Tag", "Category", "Item", "MainImage", "Images"]


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

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name


class Item(PublishedBaseModel):
    text = RichTextField(
        verbose_name="описание",
        help_text="Описание должно быть больше, чем из 2х слов и содержать"
        + " слова: превосходно, роскошно",
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

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"
        default_related_name = "items"

    def __str__(self):
        return self.name[:15]


class MainImage(django.db.models.Model):
    item = django.db.models.OneToOneField(
        Item,
        on_delete=django.db.models.CASCADE,
        related_name="main_image",
        verbose_name="товар",
    )
    image = django.db.models.ImageField(
        upload_to="catalog/main/",
        verbose_name="главное изображение",
    )

    class Meta:
        verbose_name = "главное изображение"
        verbose_name_plural = "главные изображения"

    def __str__(self):
        return f"Главное фото для {self.item.name}"

    def get_image_300x300(self):
        if self.image:
            return get_thumbnail(
                self.image,
                "300x300",
                crop="center",
                quality=90,
            )
        return None

    def image_tmb(self):
        if self.image:
            thumbnail = get_thumbnail(
                self.image,
                "50x50",
                crop="center",
                quality=90,
            )
            return mark_safe(
                f"<img src='{thumbnail.url}' width='50' height='50' "
                f"style='object-fit: cover; border-radius: 4px;' />",
            )
        return "Нет изображения"

    image_tmb.short_description = "Превью"


class Images(django.db.models.Model):
    item = django.db.models.ForeignKey(
        Item,
        on_delete=django.db.models.CASCADE,
        related_name="gallery_images",
        verbose_name="товар",
    )
    image = django.db.models.ImageField(
        upload_to="catalog/gallery/",
        verbose_name="изображение",
    )

    class Meta:
        verbose_name = "изображение галереи"
        verbose_name_plural = "изображения галереи"
        ordering = ["id"]

    def __str__(self):
        return f"Фото для {self.item.name} #{self.id}"

    def get_image_300x300(self):
        if self.image:
            return get_thumbnail(
                self.image,
                "300x300",
                crop="center",
                quality=90,
            )
        return None

    def image_tmb(self):
        if self.image:
            thumbnail = get_thumbnail(
                self.image,
                "50x50",
                crop="center",
                quality=90,
            )
            return mark_safe(
                f"<img src='{thumbnail.url}' width='50' height='50' "
                f"style='object-fit: cover; "
                f"border-radius: 4px; margin: 2px;' />",
            )
        return "Нет изображения"

    image_tmb.short_description = "Превью"
