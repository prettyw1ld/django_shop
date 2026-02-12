from django.test import Client, TestCase
from http_constants.status import HttpStatus
from django.urls import reverse


class StaticURLTests(TestCase):
    def test_homepage_endpoint(self):
        response = Client().get("/")
        self.assertEqual(response.status_code, 200)


class CoffeeViewTest(TestCase):
    def test_coffee_status_code(self):
        response = self.client.get("/coffee/")
        self.assertEqual(response.status_code, HttpStatus.I_AM_A_TEAPOT)

    def test_coffee_content(self):
        response = self.client.get("/coffee/")
        self.assertEqual(response.content.decode(), "Я чайник")
