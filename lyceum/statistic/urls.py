__all__ = ()

from django.urls import path

from statistic import views

app_name = "statistic"

urlpatterns = [
    path("", views.StatisticUserView.as_view(), name="statistic_user"),
    path(
        "<int:pk>/",
        views.StatisticItemDetailView.as_view(),
        name="statistic_item-detail",
    ),
]
