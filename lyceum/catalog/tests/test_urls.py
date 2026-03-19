__all__ = ()

from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
import parameterized


class StaticURLTests(TestCase):
    fixtures = ["data.json"]

    def test_catalog_endpoint(self):
        response = self.client.get(reverse("catalog:item-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @parameterized.parameterized.expand(
        [
            ("1", HTTPStatus.OK),
            ("4", HTTPStatus.OK),
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
    def test_catalog_item_endpoint(self, item_id, expected_status):
        try:
            url = reverse("catalog:item-detail", kwargs={"pk": item_id})
            response = self.client.get(url)
            status = response.status_code
        except Exception:
            status = HTTPStatus.NOT_FOUND

        self.assertEqual(status, expected_status)
