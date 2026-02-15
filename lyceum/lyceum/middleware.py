import re

import django.conf

WORDS_REGEX = re.compile(r"\w+|\W+")
NOT_RUSSIAN_REGEX = re.compile(r"^[^а-яА-Я\s]+$")


class ReverseRussianMiddleWare:
    cnt = 0

    def __init__(self, get_response):
        self.get_response = get_response

    @classmethod
    def check_need_reverse(cls):
        if not django.conf.settings.REVERSE_RUSSIAN:
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
        content = response.content.decode()
        words = WORDS_REGEX.findall(content)

        transformed = [
            word if NOT_RUSSIAN_REGEX.search(word) else word[::-1]
            for word in words
        ]

        response.content = "".join(transformed).encode()
        return response
