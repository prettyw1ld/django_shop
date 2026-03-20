__all__ = ()

from http import HTTPStatus

from django.db.models import F
from django.contrib.auth.decorators import login_required
import django.http
import django.shortcuts
from django.views.decorators.http import require_GET, require_POST


import catalog.models
import homepage.forms


@login_required
@require_GET
def coffee(request):
    profile = request.user.profile
    profile.coffee_count = F("coffee_count") + 1
    profile.save(update_fields=["coffee_count"])
    return django.http.HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)


def index_render(request):
    template = "homepage/main.html"
    items = catalog.models.Item.objects.on_main()
    context = {
        "items": items,
    }

    return django.shortcuts.render(request, template, context)


@require_GET
def form(request):
    template = "homepage/form.html"
    form = homepage.forms.TextForm()
    context = {"form": form}
    return django.shortcuts.render(request, template, context)


@require_POST
def echo_submit(request):
    form = homepage.forms.TextForm(request.POST)
    if form.is_valid():
        text = form.cleaned_data["text"]
        return django.http.HttpResponse(
            text,
            content_type="text/plain; charset=utf-8",
            status=HTTPStatus.OK,
        )

    return django.http.HttpResponse(
        "Invalid form data",
        status=HTTPStatus.BAD_REQUEST,
        content_type="text/plain; charset=utf-8",
    )
