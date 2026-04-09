__all__ = ()

import django.contrib.auth
import django.core.validators
import django.db.models


class Rating(django.db.models.Model):
    class Score(django.db.models.IntegerChoices):
        HATE = 1, "Ненависть"
        DISLIKE = 2, "Неприязнь"
        NEUTRAL = 3, "Нейтрально"
        ADORE = 4, "Обожание"
        LOVE = 5, "Любовь"

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
        choices=Score.choices,
        validators=[
            django.core.validators.MinValueValidator(1),
            django.core.validators.MaxValueValidator(5),
        ],
    )
    date_rate = django.db.models.DateTimeField(
        "дата оценки",
        auto_now=True,
        null=True,
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
