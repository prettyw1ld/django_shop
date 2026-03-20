__all__ = ()

import django.contrib.auth.models
import django.db.models


class User(django.contrib.auth.models.User):
    class Meta:
        proxy = True


class Profile(django.db.models.Model):
    def image_path(self, filename):
        return f"users/{self.user.id}/{filename}"

    user = django.db.models.OneToOneField(
        django.contrib.auth.models.User,
        on_delete=django.db.models.CASCADE,
    )
    bio = django.db.models.TextField(
        "о себе",
        default="",
        blank=True,
    )
    birthday = django.db.models.DateField(
        "дата рождения",
        null=True,
        blank=True,
        default=None,
    )
    image = django.db.models.ImageField(
        "аватарка",
        null=True,
        upload_to=image_path,
    )
    coffee_count = django.db.models.PositiveIntegerField(
        "количество сваренных чашек кофе",
        default=0,
        help_text="Количество попыток сварить кофе",
    )

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return f"Профиль {self.user.username}"
