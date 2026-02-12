from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("coffee/", views.coffee, name="coffee"),
]
