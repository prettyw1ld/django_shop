__all__ = []

import django.http
import django.shortcuts

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
