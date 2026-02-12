from django.test import Client, TestCase, override_settings

from .middleware import ReverseMiddleWare


class MiddleWareTest(TestCase):
    def test_middleware(self):
        ReverseMiddleWare.cont = 0
        for i in range(10):
            if i < 9:
                response = Client().get("/")
                self.assertEqual(response.content.decode(), "Главная")
            else:
                response = Client().get("/")
                self.assertEqual(response.content.decode(), "яанвалГ")

    @override_settings(ALLOW_REVERSE=False)
    def test_middleware_disabled(self):
        for i in range(10):
            response = Client().get("/")
            self.assertEqual(response.content.decode(), "Главная")
