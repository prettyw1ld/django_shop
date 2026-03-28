__all__ = ()

import django.contrib.admin

import rating.models


@django.contrib.admin.register(rating.models.Rating)
class RatingAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        rating.models.Rating.score.field.name,
        rating.models.Rating.user.field.name,
        rating.models.Rating.item.field.name,
        rating.models.Rating.date_rate.field.name,
    )
    list_display_links = (rating.models.Rating.score.field.name,)
