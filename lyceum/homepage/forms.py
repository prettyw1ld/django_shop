__all__ = ()

import django.forms


class TextForm(django.forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    text = django.forms.CharField(
        label="Обратная связь",
    )
