__all__ = ()

import django.views.generic

from catalog.models import Category, Item


class ItemListView(django.views.generic.ListView):
    template_name = "catalog/item_list.html"
    context_object_name = "items"
    queryset = Item.objects.main_image().order_by(
        f"{Item.category.field.name}__{Category.name.field.name}",
        Item.name.field.name,
    )


class ItemDetailView(django.views.generic.DetailView):
    template_name = "catalog/item.html"
    context_object_name = "item"
    queryset = Item.objects.detailed_item()


class NewItemsView(django.views.generic.ListView):
    template_name = "catalog/item_list.html"
    context_object_name = "items"
    queryset = Item.objects.new_items()


class FridayItemsView(django.views.generic.ListView):
    template_name = "catalog/item_list.html"
    context_object_name = "items"
    queryset = Item.objects.friday_items()


class UnverifiedItemsView(django.views.generic.ListView):
    template_name = "catalog/item_list.html"
    context_object_name = "items"
    queryset = Item.objects.unverified_items()
