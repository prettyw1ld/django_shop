from django.urls import path

from homepage import views

app_name = "homepage"

urlpatterns = [
    path("", views.index_render, name="index_render"),
    path("coffee/", views.coffee, name="coffee"),
]
