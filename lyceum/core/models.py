import re

import django.core.exceptions
import django.db.models
import transliterate

ONLY_LETTERS_REGEX = re.compile(r"[^\w]")


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
    cannonical_name = django.db.models.CharField(
        max_length=150,
        null=True,
        unique=True,
        editable=False,
        verbose_name="каноническое название",
        help_text="Каноническое название элемента",
    )

    def _generate_cannonical_name(self):
        try:
            transliterated = transliterate.translit(
                self.name.lower(),
                reversed=True,
            )
        except transliterate.exceptions.LanguageDetectionError:
            transliterated = self.name.lower()

        return ONLY_LETTERS_REGEX.sub(
            "",
            transliterated,
        )

    def save(self, *args, **kwargs):
        self.cannonical_name = self._generate_cannonical_name()
        super().save(*args, **kwargs)

    def clean(self):
        self.cannonical_name = self._generate_cannonical_name()
        if (
            type(self)
            .objects.filter(cannonical_name=self.cannonical_name)
            .exclude(id=self.id)
            .count()
            > 0
        ):
            raise django.core.exceptions.ValidationError(
                "Уже есть такой же элемент",
            )
        return super().clean()

    class Meta:
        abstract = True
