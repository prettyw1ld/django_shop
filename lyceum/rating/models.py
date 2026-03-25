__all__ = ()

import django.contrib.auth
import django.db.models


class Rating(django.db.models.Model):
    SCORE_CHOICES = [
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
    )
    item = django.db.models.ForeignKey(
        "catalog.Item",
        on_delete=django.db.models.CASCADE,
        related_name="ratings",
    )
    score = django.db.models.IntegerField(choices=SCORE_CHOICES)

    class Meta:
        unique_together = ("user", "item")
