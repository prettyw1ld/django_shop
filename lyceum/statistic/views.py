__all__ = ()

import django.contrib.auth.mixins
import django.db.models
import django.shortcuts
import django.views.generic

from catalog.models import Item


class StatisticUserView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.View,
):
    template_name = "statistic/statistic_user.html"

    def get(self, request):
        user = request.user
        ratings = user.ratings.all()

        context = {
            "best_item": Item.objects.best_item(user),
            "worst_item": Item.objects.worst_item(user),
            "rating_count": ratings.count(),
            "rating_avg": ratings.aggregate(
                avg=django.db.models.Avg("score"),
            )["avg"],
            "items": Item.objects.list_rated_by_user(user),
        }
        return django.shortcuts.render(request, self.template_name, context)


class StatisticItemDetailView(django.views.generic.DetailView):
    template_name = "statistic/statistic_item_detail.html"
    context_object_name = "item"
    queryset = Item.objects.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ratings = self.object.ratings.all()

        context["rating_count"] = ratings.count()
        context["rating_avg"] = ratings.aggregate(
            avg=django.db.models.Avg("score"),
        )["avg"]

        context["last_max_user"] = (
            ratings.filter(
                score=ratings.aggregate(
                    max=django.db.models.Max("score"),
                )["max"],
            )
            .order_by("-date_rate")
            .first()
        )
        context["last_min_user"] = (
            ratings.filter(
                score=ratings.aggregate(
                    min=django.db.models.Min("score"),
                )["min"],
            )
            .order_by("-date_rate")
            .first()
        )

        return context
