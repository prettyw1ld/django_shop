__all__ = ("NormalizedNameMixin", "PublishedManager", "PublishedBaseModel")

import re

import django.core.exceptions
import django.db.models
import transliterate

ONLY_LETTERS_REGEX = re.compile(r"[^\w]")


class PublishedManager(django.db.models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def published(self):
        return self.get_queryset().filter(is_published=True)

    def on_main(self):
        return self.published().filter(is_on_main=True)


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

    def _unify_similar_chars(self, text):
        text = text.lower()
        replacements = {
            "0": "o",
            "1": "l",
            "3": "e",
            "4": "a",
            "$": "s",
            "@": "a",
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

        return ONLY_LETTERS_REGEX.sub(
            "",
            transliterated,
        )

    def save(self, *args, **kwargs):
        self.canonical_name = self._generate_canonical_name()
        super().save(*args, **kwargs)

    def _save_table(self, *args, **kwargs):
        self.canonical_name = self._generate_canonical_name()
        return super()._save_table(*args, **kwargs)

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
