from http import HTTPStatus

import django.http
import django.shortcuts


def coffee(request):
    return django.http.HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)


def index_render(request):
    template = "homepage/main.html"
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
    return django.shortcuts.render(request, template, {"items": items})
