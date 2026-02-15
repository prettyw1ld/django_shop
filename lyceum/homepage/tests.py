from http import HTTPStatus

from django.test import Client, TestCase


class StaticURLTests(TestCase):
    def test_homepage_endpoint(self):
        response = Client().get("/")
        self.assertEqual(response.status_code, HTTPStatus.OK)


class CoffeeViewTest(TestCase):
    def test_coffee_status_code(self):
        response = self.client.get("/coffee/")
        self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)

    def test_coffee_content(self):
        response = self.client.get("/coffee/")
        self.assertEqual(response.content.decode(), "Я чайник")
