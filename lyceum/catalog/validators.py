import re

import django.core.validators


class ValidateMustContain:

    def __init__(self, *words):
        self.words = words

    def __call__(self, value):
        if not value:
            return

        text_lower = value.lower()
        matches = []

        for word in self.words:
            pattern = rf"\b{re.escape(word)}\b"
            if re.search(pattern, text_lower):
                matches.append(word)

        if not matches:
            raise django.core.validators.ValidationError(
                "Обязательно используйте одно из этих "
                + "слов: превосходно, роскошно",
            )

    def deconstruct(self):
        return (
            f"{self.__class__.__module__}.{self.__class__.__name__}",
            self.words,
            {},
        )


def validate_slug(value):
    if not re.match(r"^[a-zA-Z0-9_-]+$", value):
        raise django.core.validators.ValidationError(
            "Слаг должен содержать только латинские буквы,"
            + " цифры и символы '-' и '_'",
        )
    return value
