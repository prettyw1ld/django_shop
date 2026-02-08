from django.urls import path

from . import views

urlpatterns = [
    path("catalog/", views.item_list, name="item_list"),
]
