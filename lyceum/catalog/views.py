import django.http
import django.shortcuts


def item_list(request):
    template = "catalog/item_list.html"
    return django.shortcuts.render(request, template)


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
    return django.shortcuts.render(request, template, {"item": item})


def number_view(request, number):
    return django.http.HttpResponse(str(number))
