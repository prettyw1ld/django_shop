import django.http
from http import HTTPStatus


def home(request):
    return django.http.HttpResponse("<body>Главная</body>")


def coffee(request):
    return django.http.HttpResponse(
        "Я чайник", status=HTTPStatus.I_AM_A_TEAPOT
    )
