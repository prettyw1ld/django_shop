__all__ = ()

import django.db.models
import django.http
import django.shortcuts
import django.views.generic

from catalog.models import Category, Item
from rating.forms import RatingForm


class ItemListView(django.views.generic.ListView):
    template_name = "catalog/item_list.html"
    context_object_name = "items"
    queryset = Item.objects.main_image().order_by(
        f"{Item.category.field.name}__{Category.name.field.name}",
        Item.name.field.name,
    )


class ItemDetailView(django.views.generic.DetailView):
    template_name = "catalog/item.html"
    context_object_name = "item"
    queryset = Item.objects.detailed_item()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ratings = self.object.ratings.all()

        context["rating_count"] = ratings.count()
        context["rating_avg"] = ratings.aggregate(
            avg=django.db.models.Avg("score"),
        )["avg"]

        if self.request.user.is_authenticated:
            user_rating = ratings.filter(user=self.request.user).first()
            context["user_rating"] = user_rating
            context["rating_form"] = RatingForm(instance=user_rating)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not request.user.is_authenticated:
            raise django.http.Http404

        user_rating = self.object.ratings.filter(user=request.user).first()

        if "delete" in request.POST and user_rating:
            user_rating.delete()
            return django.shortcuts.redirect(request.path)

        form = RatingForm(request.POST, instance=user_rating)
        if form.is_valid():
            if form.cleaned_data["score"] is None:
                if user_rating is not None:
                    user_rating.delete()

                return django.shortcuts.redirect(request.path)

            rating = form.save(commit=False)
            rating.user = request.user
            rating.item = self.object
            rating.save()
            return django.shortcuts.redirect(request.path)

        context = self.get_context_data()
        context["rating_form"] = form
        return self.render_to_response(context)


class NewItemsView(django.views.generic.ListView):
    template_name = "catalog/item_list.html"
    context_object_name = "items"

    def get_queryset(self):
        return Item.objects.new_items()


class FridayItemsView(django.views.generic.ListView):
    template_name = "catalog/item_list.html"
    context_object_name = "items"

    def get_queryset(self):
        return Item.objects.new_items()


class UnverifiedItemsView(django.views.generic.ListView):
    template_name = "catalog/item_list.html"
    context_object_name = "items"
    queryset = Item.objects.unverified_items()
