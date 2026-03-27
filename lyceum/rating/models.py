__all__ = ()

import django.contrib.auth
import django.core.validators
import django.db.models


class Rating(django.db.models.Model):
    SCORE_CHOICES = [
        ("", "— Без оценки —"),
        (1, "Ненависть"),
        (2, "Неприязнь"),
        (3, "Нейтрально"),
        (4, "Обожание"),
        (5, "Любовь"),
    ]

    user = django.db.models.ForeignKey(
        django.contrib.auth.get_user_model(),
        on_delete=django.db.models.CASCADE,
        related_name="ratings",
        verbose_name="Пользователь",
    )
    item = django.db.models.ForeignKey(
        "catalog.Item",
        on_delete=django.db.models.CASCADE,
        related_name="ratings",
        verbose_name="товар",
    )
    score = django.db.models.PositiveSmallIntegerField(
        "оценка",
        choices=SCORE_CHOICES,
        validators=[
            django.core.validators.MinValueValidator(1),
            django.core.validators.MaxValueValidator(5),
        ],
    )

    class Meta:
        verbose_name = "рейтинг"
        verbose_name_plural = "рейтинги"
        constraints = [
            django.db.models.UniqueConstraint(
                fields=["user", "item"],
                name="unique_user_item_rating",
            ),
        ]

    def __str__(self):
        return (
            f"Пользователь {self.user.username} "
            f"поставил товару {self.item.name} оценку {self.score}"
        )
