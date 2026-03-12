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

        return (
            self.get_queryset()
            .filter(is_published=True, category__is_published=True)
            .select_related(Item.category.field.name)
            .prefetch_related(tags_prefetch)
            .only(
                Item.id.field.name,
                Item.name.field.name,
                Item.text.field.name,
                f"{Item.category.field.name}__id",
                f"{Item.category.field.name}__name",
            )
        )

    def on_main(self):
        from catalog.models import Item

        return (
            self.published()
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
        items = Item.objects.published().filter(id__in=selected_ids)
        return items

    def friday_items(self):
        from catalog.models import Item

        items = (
            Item.objects.published()
            .filter(updated__week_day=6)
            .order_by(django.db.models.F(Item.updated.field.name).desc())[
                :ITEMS_PER_PAGE
            ]
        )
        return items

    def unverified_items(self):
        from catalog.models import Item

        items = Item.objects.published().filter(
            created=django.db.models.F(Item.updated.field.name),
        )
        return items
