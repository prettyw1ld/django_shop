__all__ = []

import django.core.validators
import django.forms


class FeedbackForm(django.forms.Form):
    name = django.forms.CharField(
        max_length=150,
        label="Имя",
        validators=[
            django.core.validators.MinLengthValidator(2),
            django.core.validators.RegexValidator(
                r"^[a-zA-Zа-яА-ЯёЁ]+$",
                "Используйте только буквы",
            ),
        ],
        empty_value=True,
    )

    text = django.forms.CharField(
        label="Обратная связь",
        widget=django.forms.Textarea,
        help_text="Напишите в этом поле все то,"
        " что хотели бы сказать разработчикам",
    )

    mail = django.forms.EmailField(
        max_length=150,
        label="Почта",
        help_text="max 150 символов",
    )
