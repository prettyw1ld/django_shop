import django.forms


class TextForm(django.forms.Form):
    text = django.forms.CharField(
        label="Обратная связь",
        widget=django.forms.Textarea,
        help_text="Напишите в этом поле все то,"
        + " что хотели бы сказать разработчикам",
    )
