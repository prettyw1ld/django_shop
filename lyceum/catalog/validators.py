import re

import django.core.exceptions
import django.core.validators
import django.utils.deconstruct

__all__ = []


WORDS_REGEX = re.compile(r"\w+|\W+")


def validate_briliant(value):
    words = set(WORDS_REGEX.findall(value.lower()))
    if not {"превосходно", "роскошно"} & words:
        raise django.core.exceptions.ValidationError(
            "В тексте должно быть слово: превосходно, роскошно",
        )


@django.utils.deconstruct.deconstructible
class WordsValidator:
    def __init__(self, *args):
        self.validate_words = {word.lower() for word in args}
        self.joined_words = ", ".join(self.validate_words)

    def __call__(self, value):
        words = set(WORDS_REGEX.findall(value.lower()))
        if not self.validate_words & words:
            raise django.core.exceptions.ValidationError(
                f"В тексте {value} нет слов: {self.joined_words}",
            )
