from django.test import Client, TestCase

from catalog.models import Item


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


class CatalogItemsTests(CheckFieldTestCase):
    fixtures = ["data.json"]

    def test_items_in_context(self):
        response = Client().get("/catalog/")
        self.assertIn("items", response.context)

    def test_items_size(self):
        response = Client().get("/catalog/")
        self.assertEqual(len(response.context["items"]), 2)

    def test_items_types(self):
        response = Client().get("/catalog/")
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
        response = Client().get("/catalog/")
        for item in response.context["items"]:
            self.check_content_value(
                item,
                (
                    "name",
                    "text",
                    "is_on_main",
                    "category_id",
                    "is_published",
                ),
                ("tags",),
                (
                    "image",
                    "images",
                ),
            )


class DetailItemTests(CheckFieldTestCase):
    fixtures = ["data.json"]

    def test_items_in_context(self):
        response = Client().get("/catalog/1/")
        self.assertIn("item", response.context)

    def test_items_size(self):
        response = Client().get("/catalog/1/")
        self.assertIsInstance(response.context["item"], Item)

    def test_items_loaded_values(self):
        response = Client().get("/catalog/")
        self.check_content_value(
            response.context["item"],
            (
                "name",
                "text",
                "is_on_main",
                "category_id",
                "is_published",
            ),
            ("tags",),
            (
                "image",
                "images",
            ),
        )
        self.check_content_value(
            response.context["item"].tags.all()[0],
            ("name",),
            (),
            (),
        )
