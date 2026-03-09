__all__ = []

import datetime

import django.shortcuts
from django.utils import timezone

import catalog.models


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
    items = (
        catalog.models.Item.objects.published()
        .filter(created__gte=last_week)
        .order_by("?")[:5]
    )

    return django.shortcuts.render(
        request,
        "catalog/item_list.html",
        {"items": items, "title": "Новинки"},
    )


def friday_items(request):
    items = (
        catalog.models.Item.objects.published()
        .filter(updated__week_day=6)
        .order_by("-updated")[:5]
    )

    return django.shortcuts.render(
        request,
        "catalog/item_list.html",
        {"items": items, "title": "Пятница"},
    )


def unverified_items(request):
    from django.db.models import F

    items = catalog.models.Item.objects.published().filter(
        created=F("updated"),
    )

    return django.shortcuts.render(
        request,
        "catalog/item_list.html",
        {"items": items, "title": "Непроверенное"},
    )
