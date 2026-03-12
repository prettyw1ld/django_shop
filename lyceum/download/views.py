__all__ = ()

import django.conf
import django.http


def file(request, path):
    file_path = (django.conf.settings.MEDIA_ROOT / path).resolve()
    media_root = django.conf.settings.MEDIA_ROOT.resolve()

    if not str(file_path).startswith(str(media_root)):
        raise django.http.Http404

    if not file_path.is_file():
        raise django.http.Http404

    return django.http.FileResponse(
        open(file_path, "rb"),
        as_attachment=True,
    )
