__all__ = ()

import datetime
import random

import django.db.models
from django.utils import timezone

from core.managers import (
    PublishedManager,
)

ITEMS_PER_PAGE = 5


class ItemsManager(PublishedManager):
    def published(self):
        from catalog.models import Item, Tag

        tags_prefetch = django.db.models.Prefetch(
            Item.tags.field.name,
            queryset=Tag.objects.published().only(
                Tag.name.field.name,
            ),
        )

        published = self.get_queryset().filter(
            is_published=True,
            category__is_published=True,
        )

        return (
            published.select_related(Item.category.field.name)
            .prefetch_related(tags_prefetch)
            .defer(
                Item.is_published.field.name,
                Item.is_on_main.field.name,
            )
        )

    def main_image(self):
        return self.published().select_related("main_image")

    def detailed_item(self):
        from catalog.models import Item, Image

        return self.published().prefetch_related(
            django.db.models.Prefetch(
                Item.images.field.related_query_name(),
                queryset=Image.objects.only(
                    Image.image.field.name,
                    Image.item_id.field.name,
                ),
            ),
        )

    def on_main(self):
        from catalog.models import Item

        return (
            self.main_image()
            .filter(is_on_main=True)
            .order_by(Item.name.field.name)
        )

    def new_items(self):
        from catalog.models import Item

        last_week = timezone.now() - datetime.timedelta(days=7)
        ids = list(
            Item.objects.published()
            .filter(created__gte=last_week)
            .values_list(Item.id.field.name, flat=True),
        )

        selected_ids = random.sample(ids, min(5, len(ids)))
        return Item.objects.published().filter(id__in=selected_ids)

    def friday_items(self):
        from catalog.models import Item

        published_items = Item.objects.published()
        filtered_items = published_items.filter(updated__week_day=6)
        ordered_items = filtered_items.order_by(
            django.db.models.F(Item.updated.field.name).desc(),
        )

        return ordered_items[:ITEMS_PER_PAGE]

    def unverified_items(self):
        from catalog.models import Item

        return Item.objects.published().filter(
            created=django.db.models.F(Item.updated.field.name),
        )
