__all__ = ()

import django.forms
import django.utils.translation

from rating.models import Rating


class RatingForm(django.forms.ModelForm):
    score = django.forms.IntegerField(
        required=False,
        label=django.utils.translation.gettext_lazy("Оценка"),
        widget=django.forms.Select(
            choices=Rating.SCORE_CHOICES,
            attrs={"class": "form-select"},
        ),
    )

    class Meta:
        model = Rating
        fields = ["score"]
