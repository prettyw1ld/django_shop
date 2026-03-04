import django.shortcuts

__all__ = []


def description(request):
    template = "about/about.html"
    return django.shortcuts.render(
        request,
        template,
    )
