__all__ = []

from http import HTTPStatus

import django.http
import django.shortcuts


def coffee(request):
    return django.http.HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)


def index_render(request):
    template = "homepage/main.html"
    fake_items = [
        {"id": 1, "title": "Котик", "description": "Мягкий и пушистый"},
        {"id": 2, "title": "Собачка", "description": "Верный друг"},
        {"id": 3, "title": "Рыбка", "description": "Золотая"},
    ]

    context = {
        "items": fake_items,
    }

    return django.shortcuts.render(request, template, context)
