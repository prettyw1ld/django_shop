import django.db.models


class PublishedManager(django.db.models.Manager):
    def published(self):
        return self.get_queryset().filter(is_published=True)
