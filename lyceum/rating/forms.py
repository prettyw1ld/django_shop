__all__ = ()

import django.forms
import django.utils.translation

from rating.models import Rating


class RatingForm(django.forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["score"]
        widgets = {
            "score": django.forms.Select(attrs={"class": "form-select"}),
        }
        labels = {
            "score": django.utils.translation.gettext_lazy("Оценка"),
        }
