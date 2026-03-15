__all__ = ()

from django.conf import settings
import django.db.models


def get_upload_path(self, filename):
    return f"uploads/{self.feedback_id}/{filename}"


class FeedbackPersonalData(django.db.models.Model):
    name = django.db.models.CharField("имя", max_length=150, blank=True)
    mail = django.db.models.EmailField("почта", max_length=150)

    class Meta:
        verbose_name = "персональные данные"
        verbose_name_plural = "персональные данные"

    def __str__(self):
        return self.mail


class Feedback(django.db.models.Model):
    STATUS_CHOICES = [
        ("received", "получено"),
        ("processing", "в обработке"),
        ("answered", "ответ дан"),
    ]

    personal_data = django.db.models.OneToOneField(
        FeedbackPersonalData,
        on_delete=django.db.models.CASCADE,
        verbose_name="персональные данные",
        null=True,
    )
    text = django.db.models.TextField("обратная связь")
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
        return f"Обращение №{self.id}"


class FeedbackFile(django.db.models.Model):
    feedback = django.db.models.ForeignKey(
        Feedback,
        on_delete=django.db.models.CASCADE,
        related_name="files",
    )
    file = django.db.models.FileField("файл", upload_to=get_upload_path)


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
    to = django.db.models.CharField(
        max_length=20,
        db_column="to",
    )

    class Meta:
        verbose_name = "Статус логи"
        verbose_name_plural = "Статус логи"
