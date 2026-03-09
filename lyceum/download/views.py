import django.conf
import django.http


def file(request, path):
    return django.http.FileResponse(
        open(django.conf.settings.MEDIA_ROOT / path, "rb"),
        as_attachment=True,
    )
