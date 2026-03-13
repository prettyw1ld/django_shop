__all__ = ()

from django.conf import settings
import django.db.models


class Feedback(django.db.models.Model):
    STATUS_CHOICES = [
        ("received", "получено"),
        ("processing", "в обработке"),
        ("answered", "ответ дан"),
    ]

    name = django.db.models.CharField("имя", max_length=150, blank=True)
    text = django.db.models.TextField("обратная связь")
    mail = django.db.models.EmailField("почта", max_length=150)
    created_on = django.db.models.DateTimeField(auto_now_add=True)
    status = django.db.models.CharField(
        "статус",
        max_length=20,
        choices=STATUS_CHOICES,
        default="received",
    )

    class Meta:
        verbose_name = "обратная связь"
        verbose_name_plural = "обратные связи"

    def __str__(self):
        return f"Отзыв от {self.mail}"


class StatusLog(django.db.models.Model):
    user = django.db.models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=django.db.models.CASCADE,
        verbose_name="пользователь",
    )
    timestamp = django.db.models.DateTimeField(auto_now_add=True)
    feedback = django.db.models.ForeignKey(
        Feedback,
        on_delete=django.db.models.CASCADE,
    )
    from_status = django.db.models.CharField(
        max_length=20,
        db_column="from",
    )
    to_status = django.db.models.CharField(
        max_length=20,
        db_column="to",
    )

    class Meta:
        verbose_name = "Статус логи"
        verbose_name_plural = "Статус логи"
