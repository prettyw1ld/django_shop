__all__ = ()

import django.contrib.auth.models
import django.db.models
import sorl.thumbnail


class UserManager(django.contrib.auth.models.UserManager):
    CANONICAL_DOMAINS = {
        "ya.ru": "yandex.ru",
        "yandex.com": "yandex.ru",
    }
    DOTS = {
        "yandex.ru": "-",
        "gmail.com": "",
    }

    def get_queryset(self):
        return super().get_queryset().select_related("profile")

    def active(self):
        return self.get_queryset().filter(is_active=True)

    def by_mail(self, email):
        normalize_email = self.normalize_email(email)
        return self.active().get(email=normalize_email)

    @classmethod
    def normalize_email(cls, email):
        email = super().normalize_email(email).lower()
        try:
            email_name, domain_part = email.strip().rsplit("@", 1)
            email_name, _ = email_name.split("+", 1)

            domain_part = cls.CANONICAL_DOMAINS.get(domain_part, domain_part)
            domain_part = cls.CANONICAL_DOMAINS.get(domain_part, domain_part)

            email_name = email_name.replace(
                ".",
                cls.DOTS.get(domain_part, "."),
            )
        except ValueError:
            pass
        else:
            email = "@".join([email_name, domain_part.lower()])

        return email


class User(django.contrib.auth.models.User):
    objects = UserManager()

    class Meta:
        proxy = True


class Profile(django.db.models.Model):
    def image_path(self, filename):
        return f"users/{self.user.id}/{filename}"

    user = django.db.models.OneToOneField(
        django.contrib.auth.models.User,
        on_delete=django.db.models.CASCADE,
        verbose_name="пользователь",
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
    )
    image = django.db.models.ImageField(
        "аватарка",
        null=True,
        blank=True,
        upload_to=image_path,
    )
    coffee_count = django.db.models.PositiveIntegerField(
        "чашки кофе",
        default=0,
    )
    attempts_count = django.db.models.PositiveIntegerField(
        "попыток входа",
        default=0,
    )
    block_date = django.db.models.DateTimeField(
        "дата блокировки",
        null=True,
        blank=True,
    )

    def get_image_300x300(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            "300x300",
            crop="center",
            quality=51,
        )

    class Meta:
        verbose_name = "профиль пользователя"
        verbose_name_plural = "профили пользователей"

    def __str__(self):
        return f"Профиль {self.user.username}"
