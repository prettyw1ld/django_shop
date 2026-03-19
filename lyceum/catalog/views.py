__all__ = ()

import django.db.models
import django.shortcuts

from catalog.models import Category, Item


def item_list(request):
    template = "catalog/item_list.html"
    items = Item.objects.published().order_by(
        f"{Item.category.field.name}__{Category.name.field.name}",
        Item.name.field.name,
    )

    context = {
        "items": items,
    }
    return django.shortcuts.render(request, template, context)


def item_detail(request, pk):
    template = "catalog/item.html"
    queryset = Item.objects.detailed_item
    item = django.shortcuts.get_object_or_404(queryset, pk=pk)

    context = {
        "item": item,
    }
    return django.shortcuts.render(
        request,
        template,
        context,
    )


def new_items(request):
    template = "catalog/item_list.html"
    items = Item.objects.new_items()
    return django.shortcuts.render(
        request,
        template,
        {"items": items, "title": "Новинки"},
    )


def friday_items(request):
    template = "catalog/item_list.html"
    items = Item.objects.friday_items()
    return django.shortcuts.render(
        request,
        template,
        {"items": items, "title": "Пятница"},
    )


def unverified_items(request):
    template = "catalog/item_list.html"
    items = Item.objects.published().filter(
        created=django.db.models.F(Item.updated.field.name),
    )

    return django.shortcuts.render(
        request,
        template,
        {"items": items, "title": "Непроверенное"},
    )
