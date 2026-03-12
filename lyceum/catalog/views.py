__all__ = ()

import django.db.models
import django.shortcuts

from catalog.models import Category, Image, Item


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
    queryset = Item.objects.published().prefetch_related(
        django.db.models.Prefetch(
            Item.images.field.related_query_name(),
            queryset=Image.objects.only(
                Image.image.field.name,
                Image.item_id.field.name,
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
    items = Item.objects.new_items()
    return django.shortcuts.render(
        request,
        "catalog/item_list.html",
        {"items": items, "title": "Новинки"},
    )


def friday_items(request):
    items = Item.objects.friday_items()
    return django.shortcuts.render(
        request,
        "catalog/item_list.html",
        {"items": items, "title": "Пятница"},
    )


def unverified_items(request):
    items = Item.objects.published().filter(
        created=django.db.models.F(Item.updated.field.name),
    )

    return django.shortcuts.render(
        request,
        "catalog/item_list.html",
        {"items": items, "title": "Непроверенное"},
    )
