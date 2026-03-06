__all__ = []

from http import HTTPStatus

import django.http
import django.shortcuts

import catalog.models


def coffee(request):
    return django.http.HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)


def index_render(request):
    template = "homepage/main.html"
    items = (
        catalog.models.Item.objects.filter(is_on_main=True)
        .select_related("category")
        .prefetch_related("tags")
        .order_by("name")
    )
    context = {
        "items": items,
    }

    return django.shortcuts.render(request, template, context)
