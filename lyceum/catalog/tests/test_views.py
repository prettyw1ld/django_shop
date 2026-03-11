__all__ = ()

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
        self.assertEqual(len(response.context["items"]), 5)

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
                    "category_id",
                ),
                ("tags",),
                (
                    "is_published",
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
                "category_id",
            ),
            ("tags",),
            (
                "is_published",
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


class CatalogFridayItemsTests(CheckFieldTestCase):
    fixtures = ["data.json"]

    def test_friday_items_in_context(self):
        response = Client().get("/catalog/friday/")
        self.assertIn("items", response.context)

    def test_friday_items_size(self):
        response = Client().get("/catalog/friday/")
        self.assertEqual(len(response.context["items"]), 0)

    def test_friday_items_types(self):
        response = Client().get("/catalog/friday/")
        self.assertTrue(
            all(
                isinstance(
                    item,
                    Item,
                )
                for item in response.context["items"]
            ),
        )

    def test_friday_items_loaded_values(self):
        response = Client().get("/catalog/friday/")
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


class CatalogNewItemsTests(CheckFieldTestCase):
    fixtures = ["data.json"]

    def test_new_items_in_context(self):
        response = Client().get("/catalog/new/")
        self.assertIn("items", response.context)

    def test_new_items_size(self):
        response = Client().get("/catalog/new/")
        self.assertEqual(len(response.context["items"]), 5)

    def test_new_items_types(self):
        response = Client().get("/catalog/new/")
        self.assertTrue(
            all(
                isinstance(
                    item,
                    Item,
                )
                for item in response.context["items"]
            ),
        )

    def test_new_items_loaded_values(self):
        response = Client().get("/catalog/new/")
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


class CatalogUnverifiedNewItemsTests(CheckFieldTestCase):
    fixtures = ["data.json"]

    def test_unverified_items_in_context(self):
        response = Client().get("/catalog/unverified/")
        self.assertIn("items", response.context)

    def test_unverified_items_size(self):
        response = Client().get("/catalog/unverified/")
        self.assertEqual(len(response.context["items"]), 4)

    def test_unverified_items_types(self):
        response = Client().get("/catalog/unverified/")
        self.assertTrue(
            all(
                isinstance(
                    item,
                    Item,
                )
                for item in response.context["items"]
            ),
        )

    def test_unverified_items_loaded_values(self):
        response = Client().get("/catalog/unverified/")
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
