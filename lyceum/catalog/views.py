import django.http
import django.shortcuts

__all__ = []


def item_list(request):
    template = "catalog/item_list.html"
    items = [
        {
            "id": 1,
            "title": "Сонный деник",
            "description": "Надудонился и спит",
        },
        {
            "id": 2,
            "title": "Люксовый",
            "description": "Слишком дорого чтобы объяснять",
        },
        {"id": 3, "title": "Депресивни", "description": "Грустни(("},
    ]
    return django.shortcuts.render(
        request,
        template,
        {
            "items": items,
            "active_menu": "catalog",
        },
    )


def item_detail(request, pk):
    template = "catalog/item.html"
    items = {
        1: {
            "id": 1,
            "title": "Сонный деник",
            "description": "Надудонился и спит",
        },
        2: {
            "id": 2,
            "title": "Люксовый",
            "description": "Слишком дорого чтобы объяснять",
        },
        3: {"id": 3, "title": "Депресивни", "description": "Грустни(("},
    }
    item = items.get(pk)
    return django.shortcuts.render(
        request,
        template,
        {
            "item": item,
            "active_menu": "catalog",
        },
    )


def number_view(request, number):
    return django.http.HttpResponse(str(number))
