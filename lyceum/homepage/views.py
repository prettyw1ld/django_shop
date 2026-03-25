__all__ = ()

from http import HTTPStatus

from django.db.models import F
import django.http
import django.shortcuts
import django.views.generic


import catalog.models
import homepage.forms


class CoffeeView(django.views.generic.View):
    def get(self, request):
        if request.user.is_authenticated:
            profile = request.user.profile
            profile.coffee_count = F("coffee_count") + 1
            profile.save(update_fields=["coffee_count"])

        return django.http.HttpResponse(
            "Я чайник",
            status=HTTPStatus.IM_A_TEAPOT,
        )


class IndexView(django.views.generic.TemplateView):
    template_name = "homepage/main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = catalog.models.Item.objects.on_main()
        return context


class FormView(django.views.generic.FormView):
    template_name = "homepage/form.html"
    form_class = homepage.forms.TextForm

    def form_valid(self, form):
        text = form.cleaned_data["text"]
        return django.http.HttpResponse(
            text,
            content_type="text/plain; charset=utf-8",
            status=HTTPStatus.OK,
        )

    def form_invalid(self, form):
        return django.http.HttpResponse(
            "Invalid form data",
            status=HTTPStatus.BAD_REQUEST,
            content_type="text/plain; charset=utf-8",
        )


class EchoView(django.views.generic.View):
    def get(self, request):
        form = homepage.forms.TextForm()
        return django.shortcuts.render(
            request,
            "homepage/form.html",
            {"form": form},
        )

    def post(self, request):
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
