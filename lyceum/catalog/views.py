__all__ = []

import django.http
import django.shortcuts


def item_list(request):
    template = "catalog/item_list.html"
    fake_items = [
        {"id": 1, "title": "Котик", "description": "Мягкий и пушистый"},
        {"id": 2, "title": "Собачка", "description": "Верный друг"},
        {"id": 3, "title": "Рыбка", "description": "Золотая"},
    ]

    context = {
        "items": fake_items,
    }

    return django.shortcuts.render(request, template, context)


def item_detail(request, pk):
    template = "catalog/item.html"
    fake_items = {
        1: {"id": 1, "title": "Котик", "description": "Мягкий и пушистый"},
        2: {"id": 2, "title": "Собачка", "description": "Верный друг"},
        3: {"id": 3, "title": "Рыбка", "description": "Золотая"},
    }
    item = fake_items.get(int(pk), fake_items[1])

    return django.shortcuts.render(request, template, {"item": item})
