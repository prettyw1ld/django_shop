from http import HTTPStatus

import django.http
import django.shortcuts

__all__ = []


def coffee(request):
    return django.http.HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)


def index_render(request):
    template = "homepage/main.html"
    return django.shortcuts.render(request, template)
