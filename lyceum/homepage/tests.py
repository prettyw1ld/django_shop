__all__ = []

from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse


class StaticURLTests(TestCase):
    def test_homepage_endpoint(self):
        response = Client().get(reverse("homepage:home"))
        self.assertEqual(response.status_code, HTTPStatus.OK)


class CoffeeViewTest(TestCase):
    def test_coffee_status_code(self):
        response = self.client.get(reverse("homepage:coffee"))
        self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)
        self.assertEqual(response.content.decode(), "Я чайник")
