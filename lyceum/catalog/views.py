import django.http
import django.shortcuts

__all__ = []


def item_list(request):
    template = "catalog/item_list.html"
    return django.shortcuts.render(request, template)


def item_detail(request, pk):
    template = "catalog/item.html"
    return django.shortcuts.render(request, template)


def number_view(request, number):
    return django.http.HttpResponse(str(number))
