__all__ = []

import re

import django.core.exceptions
import django.db.models
import transliterate

ONLY_LETTERS_REGEX = re.compile(r"[^\w]")


class NormalizedNameMixin(django.db.models.Model):
    canonical_name = django.db.models.CharField(
        max_length=150,
        null=True,
        unique=True,
        editable=False,
        verbose_name="каноническое название",
        help_text="Каноническое название элемента",
    )

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
        super().save(*args, **kwargs)

    def clean(self):
        self.canonical_name = self._generate_canonical_name()
        if (
            type(self)
            .objects.filter(canonical_name=self.canonical_name)
            .exclude(id=self.id)
            .exists()
        ):
            raise django.core.exceptions.ValidationError(
                "Уже есть такой же элемент",
            )
        return super().clean()

    class Meta:
        abstract = True


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
