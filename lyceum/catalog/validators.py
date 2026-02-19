import re

import django.core.validators


def validate_brilliant(value):
    match_1 = re.search(r"\bпревосходно\b", value.lower())
    match_2 = re.search(r"\bроскошно\b", value.lower())
    if not match_1 and not match_2:
        raise django.core.validators.ValidationError(
            "Обязательно используйте одно из этих "
            + "слов: превосходно, роскошно",
        )
    return value


def validate_slug(value):
    if not re.match(r"^[a-zA-Z0-9_-]+$", value):
        raise django.core.validators.ValidationError(
            "Слаг должен содержать только латинские буквы,"
            + " цифры и символы '-' и '_'",
        )
    return value
