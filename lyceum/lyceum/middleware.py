__all__ = ()

import re

from django.conf import settings

RUSSIAN_WORD_REGEX = re.compile(r"[а-яА-ЯёЁ]+")


class ReverseRussianMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not getattr(settings, "ALLOW_REVERSE", False):
            return response

        content_type = response.get("Content-Type", "")
        if "text/html" in content_type or "text/plain" in content_type:
            content = response.content.decode(response.charset)

            def replace_func(match):
                return match.group()[::-1]

            transformed = RUSSIAN_WORD_REGEX.sub(replace_func, content)
            response.content = transformed.encode(response.charset)
            if "Content-Length" in response:
                response["Content-Length"] = str(len(response.content))

        return response
