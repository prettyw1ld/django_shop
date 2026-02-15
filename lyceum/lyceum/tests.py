from django.test import Client, override_settings, TestCase

from .middleware import ReverseRussianMiddleWare


class MiddleWareTest(TestCase):
    def test_middleware(self):
        ReverseRussianMiddleWare.cnt = 0
        for i in range(10):
            if i < 9:
                response = Client().get("/")
                self.assertEqual(response.content.decode(), "Главная")
            else:
                response = self.client.get("/")
                self.assertEqual(response.content.decode(), "яанвалГ")

    @override_settings(REVERSE_RUSSIAN=False)
    def test_middleware_disabled(self):
        for i in range(10):
            response = Client().get("/")
            self.assertEqual(response.content.decode(), "Главная")
