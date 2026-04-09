__all__ = ()

import re
import zoneinfo

import django.conf
from django.utils import timezone

WORDS_REGEX = re.compile(r"\w+|\W+")
RUSSIAN_WORD_REGEX = re.compile(r"^[а-яА-ЯёЁ]+$")


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
        content = response.content.decode()
        words = WORDS_REGEX.findall(content)

        transformed = [
            word[::-1] if RUSSIAN_WORD_REGEX.search(word) else word
            for word in words
        ]

        response.content = "".join(transformed).encode("utf-8")
        return response


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            tzname = request.COOKIES.get("django_timezone")
            if tzname:
                timezone.activate(zoneinfo.ZoneInfo(tzname))
            else:
                timezone.deactivate()

        except Exception:
            timezone.deactivate()

        return self.get_response(request)
