from http import HTTPStatus

import django.http
import django.shortcuts


def home(request):
    return django.http.HttpResponse("Главная")


def coffee(request):
    return django.http.HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)


def index_render(request):
    template = "homepage/home.html"
    return django.shortcuts.render(request, template)
