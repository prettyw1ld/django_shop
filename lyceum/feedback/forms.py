__all__ = ()

import django.forms

from feedback.models import Feedback, FeedbackPersonalData


class MultipleFileInput(django.forms.FileInput):
    allow_multiple_selected = True


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


class PersonalDataForm(django.forms.ModelForm):
    class Meta:
        model = FeedbackPersonalData
        exclude = ("id",)
        labels = {"name": "Имя", "mail": "Почта"}


class FeedbackContentForm(django.forms.ModelForm):
    class Meta:
        model = Feedback
        exclude = ("id", "created_on", "status", "personal_data")
        labels = {"text": "Обратная связь"}


class FeedbackFileForm(django.forms.Form):
    files = MultipleFileField(label="Файлы", required=False)
