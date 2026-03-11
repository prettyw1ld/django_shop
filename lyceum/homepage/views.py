__all__ = []

from http import HTTPStatus

import django.http
import django.shortcuts

import catalog.models
import homepage.forms


def coffee(request):
    return django.http.HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)


def index_render(request):
    template = "homepage/main.html"
    items = (
        catalog.models.Item.objects.filter(is_on_main=True)
        .select_related("category")
        .prefetch_related("tags")
        .order_by("name")
    )
    context = {
        "items": items,
    }

    return django.shortcuts.render(request, template, context)


def form(request):
    template = "homepage/form.html"
    form = homepage.forms.TextForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        text = form.cleaned_data["text"]
        return django.shortcuts.redirect(
            f"{django.shortcuts.reverse("homepage:echo-submit")}?text={text}",
        )

    context = {
        "form": form,
    }
    return django.shortcuts.render(request, template, context)


def echo_submit(request):
    text = request.POST.get("text")
    return django.http.HttpResponse(
        text,
        content_type="text/plain; charset=utf-8",
        status=HTTPStatus.OK,
    )
