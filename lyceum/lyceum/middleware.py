__all__ = ()

import re

import django.conf

RUSSIAN_WORD_REGEX = re.compile(r"[а-яА-ЯёЁ]+")


class ReverseRussianMiddleware:
    cnt = 0

    def __init__(self, get_response):
        self.get_response = get_response

    @classmethod
    def check_need_reverse(cls):
        if not django.conf.settings.ALLOW_REVERSE:
            return False

        cls.cnt += 1
        if cls.cnt != 10:
            return False

        cls.cnt = 0
        return True

    def __call__(self, request):
        if not self.check_need_reverse():
            return self.get_response(request)

        response = self.get_response(request)
        content = response.content.decode(response.charset)

        def replace_func(match):
            word = match.group()
            return word[::-1]

        transformed = RUSSIAN_WORD_REGEX.sub(replace_func, content)

        response.content = transformed.encode("utf-8")
        return response
