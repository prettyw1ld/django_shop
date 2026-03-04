__all__ = []

from http import HTTPStatus

import django.test
from django.urls import reverse


class StaticURLTests(django.test.TestCase):
    def test_about_endpoint(self):
        response = self.client.get(reverse("about:about"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
