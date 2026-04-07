from django.urls import path

from homepage import views

app_name = "homepage"

urlpatterns = [
    path("", views.IndexView.as_view(), name="home"),
    path("coffee/", views.CoffeeView.as_view(), name="coffee"),
    path("echo/", views.FormView.as_view(), name="echo-form"),
    path("echo/submit/", views.EchoView.as_view(), name="echo-submit"),
]
