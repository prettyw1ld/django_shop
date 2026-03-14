__all__ = ()

import django.forms

from feedback.models import Feedback


class FeedbackForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Feedback
        exclude = ("id", "created_on", "status")
        labels = {
            "name": "Имя",
            "text": "Обратная связь",
            "mail": "Почта",
        }
        help_texts = {
            "text": "Напишите в этом поле все то, "
            "что хотели бы сказать разработчикам",
            "mail": "max 150 символов",
        }
