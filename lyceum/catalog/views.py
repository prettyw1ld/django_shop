__all__ = []

import django.http
import django.shortcuts

import catalog.models


def item_list(request):
    template = "catalog/item_list.html"
    items = (
        catalog.models.Item.objects.filter(is_published=True)
        .select_related("category")
        .prefetch_related("tags")
        .order_by("category__name", "name")
    )

    context = {
        "items": items,
    }
    return django.shortcuts.render(request, template, context)


def item_detail(request, pk):
    template = "catalog/item.html"
    item = django.shortcuts.get_object_or_404(
        catalog.models.Item.objects.filter(is_published=True)
        .select_related("category", "main_image")
        .prefetch_related("tags", "images"),
        pk=pk,
    )
    context = {
        "item": item,
    }
    return django.shortcuts.render(request, template, context)
