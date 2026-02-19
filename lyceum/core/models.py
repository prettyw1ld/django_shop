import django.db.models


class PublishedBaseModel(django.db.models.Model):
    is_published = django.db.models.BooleanField(
        default=True, verbose_name="Опубликовано",
    )

    class Meta:
        abstract = True
