from http import HTTPStatus

from django.test import Client, TestCase
import parameterized


class StaticURLTests(TestCase):
    fixtures = ["data.json"]

    def test_catalog_endpoint(self):
        response = self.client.get("/catalog/")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @parameterized.parameterized.expand(
        [
            ("1", HTTPStatus.OK),
            ("4", HTTPStatus.NOT_FOUND),
            ("100", HTTPStatus.NOT_FOUND),
            ("0", HTTPStatus.NOT_FOUND),
            ("-0", HTTPStatus.NOT_FOUND),
            ("-100", HTTPStatus.NOT_FOUND),
            ("0.5", HTTPStatus.NOT_FOUND),
            ("abc", HTTPStatus.NOT_FOUND),
            ("0abc", HTTPStatus.NOT_FOUND),
            ("abc0", HTTPStatus.NOT_FOUND),
            ("$#@", HTTPStatus.NOT_FOUND),
            ("1e5", HTTPStatus.NOT_FOUND),
        ],
    )
    def test_catalog_item_endpoint(self, url, expected_status):
        response = Client().get(f"/catalog/{url}/")
        self.assertEqual(response.status_code, expected_status)
