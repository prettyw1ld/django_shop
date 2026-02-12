import django.http
from http_constants.status import HttpStatus

def home(request):
    return django.http.HttpResponse("<body>Главная</body>")

def coffee(request):
    return django.http.response("<body>Я чайник</body>", status=HttpStatus.I_AM_A_TEAPOT)