from http import HTTPStatus

import django.test


class StaticURLTests(django.test.TestCase):
    def test_about_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
