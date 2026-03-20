__all__ = ("NormalizedNameMixin", "PublishedBaseModel", "ImageBaseModel")

import re

import django.core.exceptions
import django.db.models
from sorl.thumbnail import get_thumbnail
import transliterate

ONLY_LETTERS_REGEX = re.compile(r"[^\w]")


def item_directory_path(instance, filename):
    return f"catalog/{instance.item.id}/{filename}"


class NormalizedNameMixin(django.db.models.Model):
    canonical_name = django.db.models.CharField(
        max_length=150,
        default="",
        blank=True,
        unique=True,
        editable=False,
        verbose_name="каноническое название",
        help_text="Каноническое название элемента",
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.canonical_name = self._generate_canonical_name()
        super().save(*args, **kwargs)

    def clean(self):
        self.canonical_name = self._generate_canonical_name()
        exists = (
            type(self)
            .objects.filter(canonical_name=self.canonical_name)
            .exclude(id=self.id)
            .exists()
        )
        if exists:
            raise django.core.exceptions.ValidationError(
                "Уже есть такой же элемент",
            )

        return super().clean()

    def _unify_similar_chars(self, text):
        text = text.lower()
        replacements = {
            "0": "o",
            "i": "l",
            "1": "l",
            "3": "e",
            "4": "a",
            "8": "b",
            "$": "s",
            "@": "a",
            "ё": "e",
            "е": "e",
            "й": "и",
            "з": "3",
            "р": "p",
            "ъ": "b",
            "ь": "b",
        }
        for wrong, correct in replacements.items():
            text = text.replace(wrong, correct)

        return text

    def _generate_canonical_name(self):
        unified = self._unify_similar_chars(self.name)
        try:
            transliterated = transliterate.translit(unified, reversed=True)
        except transliterate.exceptions.LanguageDetectionError:
            transliterated = unified

        return ONLY_LETTERS_REGEX.sub("", transliterated)

    def _save_table(self, *args, **kwargs):
        self.canonical_name = self._generate_canonical_name()
        return super()._save_table(*args, **kwargs)


class PublishedBaseModel(django.db.models.Model):
    name = django.db.models.CharField(
        max_length=150,
        verbose_name="название",
        help_text="max 150 символов",
        unique=True,
    )
    is_published = django.db.models.BooleanField(
        default=True,
        verbose_name="опубликовано",
        help_text="статус публикации",
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name[:15]


class ImageBaseModel(django.db.models.Model):
    image = django.db.models.ImageField(
        "изображение",
        upload_to=item_directory_path,
        default=None,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.image.name[:15]

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
