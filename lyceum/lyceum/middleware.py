from django.conf import settings


class ReverseMiddleWare:
    cont = 0

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if settings.ALLOW_REVERSE:
            ReverseMiddleWare.cont += 1
            if ReverseMiddleWare.cont == 10:
                content = response.content.decode()
                words = content.split()
                reversed_words = [word[::-1] for word in words]
                new_content = " ".join(reversed_words)
                response.content = new_content
                ReverseMiddleWare.cont = 0
                return response
            else:
                return response
        else:
            return response
