import re

import django.core.validators


def validate_brilliant(value):
    must_be_word_1 = "превосходно"
    must_be_word_2 = "роскошно"
    if (
        must_be_word_1 not in value.lower()
        and must_be_word_2 not in value.lower()
    ):
        raise django.core.validators.ValidationError(
            "Обязательно используйте одно из этих "
            + f"слов: {must_be_word_1}, {must_be_word_2}",
        )
    return value


def validate_slug(value):
    if not re.match(r"^[a-zA-Z0-9_-]+$", value):
        raise django.core.validators.ValidationError(
            "Слаг должен содержать только латинские буквы,"
            + " цифры и символы '-' и '_'",
        )
    return value
