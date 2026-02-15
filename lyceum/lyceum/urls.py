from django import conf, urls
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("catalog/", include("catalog.urls")),
    path("about/", include("about.urls")),
    path("", include("homepage.urls")),
]


if conf.settings.DEBUG:
    import debug_toolbar

    urlpatterns += (urls.path("__debug__/", urls.include(debug_toolbar.urls)),)
