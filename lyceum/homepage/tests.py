__all__ = ()

from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from catalog.models import Item


class StaticURLTests(TestCase):
    def test_homepage_endpoint(self):
        response = Client().get(reverse("homepage:home"))
        self.assertEqual(response.status_code, HTTPStatus.OK)


class CoffeeViewTest(TestCase):
    def test_coffee_status_code(self):
        response = self.client.get(reverse("homepage:coffee"))
        self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)
        self.assertEqual(response.content.decode(), "Я чайник")


class CheckFieldTestCase(TestCase):
    def check_content_value(
        self,
        item,
        exists,
        prefetched,
        not_loaded,
    ):
        check_dict = item.__dict__

        for value in exists:
            self.assertIn(value, check_dict)

        for value in prefetched:
            self.assertIn(value, check_dict["_prefetched_objects_cache"])

        for value in not_loaded:
            self.assertNotIn(value, check_dict)


class HomepageItemsTests(CheckFieldTestCase):
    fixtures = ["data.json"]

    def test_items_in_context(self):
        response = Client().get("/")
        self.assertIn("items", response.context)

    def test_items_size(self):
        response = Client().get("/")
        self.assertEqual(len(response.context["items"]), 4)

    def test_items_types(self):
        response = Client().get("/")
        self.assertTrue(
            all(
                isinstance(
                    item,
                    Item,
                )
                for item in response.context["items"]
            ),
        )

    def test_items_loaded_values(self):
        response = Client().get("/")
        for item in response.context["items"]:
            self.check_content_value(
                item,
                (
                    "name",
                    "text",
                    "category_id",
                ),
                ("tags",),
                (
                    "is_published",
                    "image",
                    "images",
                ),
            )
