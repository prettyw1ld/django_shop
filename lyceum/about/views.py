import django.http
import django.shortcuts


def description(request):
    template = "about/about.html"
    return django.shortcuts.render(request, template)
