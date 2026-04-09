from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
import django.contrib.auth.urls
from django.urls import include, path

import users.urls

urlpatterns = [
    path("", include("homepage.urls")),
    path("about/", include("about.urls")),
    path("admin/", admin.site.urls),
    path("auth/", include(users.urls)),
    path("auth/", include(django.contrib.auth.urls)),
    path("catalog/", include("catalog.urls")),
    path("download/", include("download.urls")),
    path("feedback/", include("feedback.urls")),
    path("statistic/", include("statistic.urls")),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
]

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += debug_toolbar_urls()
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
