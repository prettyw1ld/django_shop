import django.http
from http_constants.status import HttpStatus


def home(request):
    return django.http.HttpResponse("<body>Popa</body>")


def coffee(request):
    return django.http.HttpResponse(
        "Я чайник", status=HttpStatus.I_AM_A_TEAPOT
    )
