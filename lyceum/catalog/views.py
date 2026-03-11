__all__ = ()

import datetime
import random

import django.db.models
import django.shortcuts
from django.utils import timezone

import catalog.models

ITEMS_PER_PAGE = 5


def item_list(request):
    template = "catalog/item_list.html"
    items = catalog.models.Item.objects.published().order_by(
        "category__name",
        "name",
    )

    context = {
        "items": items,
    }
    return django.shortcuts.render(request, template, context)


def item_detail(request, pk):
    queryset = catalog.models.Item.objects.published().prefetch_related(
        django.db.models.Prefetch(
            catalog.models.Item.images.field.related_query_name(),
            queryset=catalog.models.Image.objects.only(
                catalog.models.Image.image.field.name,
                catalog.models.Image.item_id.field.name,
            ),
        ),
    )
    item = django.shortcuts.get_object_or_404(queryset, pk=pk)

    context = {
        "item": item,
    }
    return django.shortcuts.render(
        request,
        "catalog/item.html",
        context,
    )


def new_items(request):
    last_week = timezone.now() - datetime.timedelta(days=7)
    ids = list(
        catalog.models.Item.objects.published()
        .filter(created__gte=last_week)
        .values_list("id", flat=True),
    )

    selected_ids = random.sample(ids, min(5, len(ids)))
    items = catalog.models.Item.objects.published().filter(id__in=selected_ids)
    return django.shortcuts.render(
        request,
        "catalog/item_list.html",
        {"items": items, "title": "Новинки"},
    )


def friday_items(request):
    items = (
        catalog.models.Item.objects.published()
        .filter(updated__week_day=6)
        .order_by("-updated")[:ITEMS_PER_PAGE]
    )

    return django.shortcuts.render(
        request,
        "catalog/item_list.html",
        {"items": items, "title": "Пятница"},
    )


def unverified_items(request):
    items = catalog.models.Item.objects.published().filter(
        created=django.db.models.F("updated"),
    )

    return django.shortcuts.render(
        request,
        "catalog/item_list.html",
        {"items": items, "title": "Непроверенное"},
    )
