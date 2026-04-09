from django.urls import path

from catalog import views

app_name = "catalog"

urlpatterns = [
    path("", views.ItemListView.as_view(), name="item-list"),
    path("<int:pk>/", views.ItemDetailView.as_view(), name="item-detail"),
    path("new/", views.NewItemsView.as_view(), name="new-items"),
    path("friday/", views.FridayItemsView.as_view(), name="friday-items"),
    path(
        "unverified/",
        views.UnverifiedItemsView.as_view(),
        name="unverified-items",
    ),
]
