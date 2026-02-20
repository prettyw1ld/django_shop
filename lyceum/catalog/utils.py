import django.utils.text
from transliterate import translit


def normalization_function(raw_name):
    clear_name = raw_name.strip().lower()
    return django.utils.text.slugify(translit(clear_name, "ru", reversed=True))
