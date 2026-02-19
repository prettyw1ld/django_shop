from django.urls import path, re_path, register_converter

from catalog import converters
from catalog import views

register_converter(converters.PositiveIntegerConverter, "positive_int")

urlpatterns = [
    path("", views.item_list, name="item_list"),
    path("<int:pk>/", views.item_detail, name="item_detail"),
    re_path(
        r"^re/(?P<number>0*[1-9]\d*)/$", views.number_view, name="re_number",
    ),
    path(
        "converter/<positive_int:number>/",
        views.number_view,
        name="converter_number",
    ),
]
