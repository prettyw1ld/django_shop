from http import HTTPStatus
import itertools

from django.test import Client, TestCase
import parameterized


class StaticURLTests(TestCase):
    def test_catalog_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @parameterized.parameterized.expand(
        [
            ("1", HTTPStatus.OK),
            ("100", HTTPStatus.OK),
            ("0", HTTPStatus.OK),
            ("-0", HTTPStatus.NOT_FOUND),
            ("-100", HTTPStatus.NOT_FOUND),
            ("0.5", HTTPStatus.NOT_FOUND),
            ("abc", HTTPStatus.NOT_FOUND),
            ("0abc", HTTPStatus.NOT_FOUND),
            ("abc0", HTTPStatus.NOT_FOUND),
            ("$#@", HTTPStatus.NOT_FOUND),
            ("1e5", HTTPStatus.NOT_FOUND),
            ("1_1", HTTPStatus.NOT_FOUND),
            ("१२३", HTTPStatus.NOT_FOUND),
        ]
    )
    def test_catalog_item_endpoint(self, url, expected_status):
        response = Client().get(f"/catalog/{url}/")
        self.assertEqual(response.status_code, expected_status)

    @parameterized.parameterized.expand(
        map(
            lambda x: (x[0], x[1][0], x[1][1]),
            itertools.product(
                [
                    "converter",
                    "re",
                ],
                [
                    ("1", HTTPStatus.OK),
                    ("100", HTTPStatus.OK),
                    ("0", HTTPStatus.NOT_FOUND),
                    ("-0", HTTPStatus.NOT_FOUND),
                    ("-100", HTTPStatus.NOT_FOUND),
                    ("0.5", HTTPStatus.NOT_FOUND),
                    ("abc", HTTPStatus.NOT_FOUND),
                    ("0abc", HTTPStatus.NOT_FOUND),
                    ("abc0", HTTPStatus.NOT_FOUND),
                    ("$#@", HTTPStatus.NOT_FOUND),
                    ("1e5", HTTPStatus.NOT_FOUND),
                    ("1_1", HTTPStatus.NOT_FOUND),
                    ("१२३", HTTPStatus.NOT_FOUND),
                ],
            ),
        )
    )
    def test_catalog_item_positive_integer_endpoint(
        self,
        prefix,
        url,
        expected_status,
    ):
        full_url = f"/catalog/{prefix}/{url}/"
        response = self.client.get(full_url)
        self.assertEqual(
            response.status_code,
            expected_status,
            f"failed check status request to '{full_url}'",
        )
