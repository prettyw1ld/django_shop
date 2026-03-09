from django.urls import path

from catalog import views

app_name = "catalog"

urlpatterns = [
    path("", views.item_list, name="item-list"),
    path("<int:pk>/", views.item_detail, name="item-detail"),
    path("new/", views.new_items, name="new_items"),
    path("friday/", views.friday_items, name="friday_items"),
    path("unverified/", views.unverified_items, name="unverified_items"),
]
