__all__ = ()

import django.forms

from feedback.models import Feedback


class MultipleFileInput(django.forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(django.forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_file_clean(d, initial) for d in data]

        return single_file_clean(data, initial)


class FeedbackForm(django.forms.ModelForm):
    name = django.forms.CharField(label="Имя", max_length=150, required=False)
    mail = django.forms.EmailField(
        label="Почта",
        max_length=150,
        help_text="max 150 символов",
    )
    files = MultipleFileField(label="Файлы", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

        self.fields["files"].widget.attrs["multiple"] = True

    class Meta:
        model = Feedback
        fields = ("text",)
        labels = {"text": "Обратная связь"}
        help_texts = {
            "text": "Напишите в этом поле все то,"
            " что хотели бы сказать разработчикам",
        }
