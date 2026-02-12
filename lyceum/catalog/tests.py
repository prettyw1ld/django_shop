from django.test import Client, TestCase
from django.urls import reverse


class StaticURLTests(TestCase):
    def test_catalog_endpoint(self):
        response = Client().get("/")
        self.assertEqual(response.status_code, 200)


class NumberRePathTest(TestCase):
    def test_valid_number(self):
        response = self.client.get(
            reverse("re_number", kwargs={"number": 123})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "123")


class PositiveIntConverterTest(TestCase):
    def test_int_converter(self):
        response = self.client.get(
            reverse("converter_number", kwargs={"number": 456})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "456")
