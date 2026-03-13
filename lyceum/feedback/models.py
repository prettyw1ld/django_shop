__all__ = ()

import django.db.models


class Feedback(django.db.models.Model):
    name = django.db.models.CharField(
        max_length=150,
        verbose_name="имя",
        help_text="max 150 символов",
        blank=True,
    )
    text = django.db.models.TextField(
        verbose_name="обратная связь",
        help_text="Напишите в этом поле все то,"
        " что хотели бы сказать разработчикам",
    )
    created_on = django.db.models.DateTimeField(
        verbose_name="время создания",
        auto_now_add=True,
    )
    mail = django.db.models.EmailField(
        max_length=150,
        verbose_name="почта",
        help_text="max 150 символов",
    )

    class Meta:
        verbose_name = "обратная связь"
        verbose_name_plural = "обратная связь"

    def __str__(self):
        return f"Обратная связь от {self.name} ({self.mail})"
