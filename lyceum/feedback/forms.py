__all__ = ()

import django.forms
from django.utils.translation import gettext_lazy as _

from feedback.models import Feedback, FeedbackPersonalData


class MultipleFileInput(django.forms.FileInput):
    allow_multiple_selected = True


class CssModelForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class MultipleFileField(django.forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault(
            "widget",
            MultipleFileInput(attrs={"multiple": True}),
        )
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_file_clean(d, initial) for d in data]

        return single_file_clean(data, initial)


class PersonalDataForm(CssModelForm):
    class Meta:
        model = FeedbackPersonalData
        exclude = ("id",)
        labels = {
            "name": _("Имя"),
            "mail": _("Почта"),
        }
        help_texts = {
            "name": _("Введите ваше имя"),
            "mail": _("Введите ваш email"),
        }


class FeedbackContentForm(CssModelForm):
    class Meta:
        model = Feedback
        exclude = ("id", "created_on", "status", "personal_data")
        labels = {"text": _("Обратная связь")}
        help_texts = {
            "text": _("Напишите ваш отзыв"),
        }


class FeedbackFileForm(django.forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    files = MultipleFileField(
        label=_("Файлы"),
        required=False,
        help_text=_("Прикрепите файлы к отзыву"),
    )
