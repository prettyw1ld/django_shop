from django.urls import path

from homepage import views

app_name = "homepage"

urlpatterns = [
    path("", views.index_render, name="home"),
    path("coffee/", views.coffee, name="coffee"),
    path("echo/", views.form, name="form"),
    path("echo_submit", views.echo_submit, name="echo_submit"),
]
