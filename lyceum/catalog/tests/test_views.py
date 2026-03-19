__all__ = ()

from django.test import TestCase
from django.urls import reverse

from catalog.models import Image, Item, MainImage, Tag


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
        response = self.client.get(reverse("catalog:item-list"))
        self.assertIn("items", response.context)

    def test_items_size(self):
        response = self.client.get(reverse("catalog:item-list"))
        self.assertEqual(len(response.context["items"]), 5)

    def test_items_types(self):
        response = self.client.get(reverse("catalog:item-list"))
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
        response = self.client.get(reverse("catalog:item-list"))
        for item in response.context["items"]:
            self.check_content_value(
                item,
                (
                    Item.name.field.name,
                    Item.text.field.name,
                    Item.category.field.attname,
                ),
                (Item.tags.field.name,),
                (
                    Item.is_published.field.name,
                    MainImage.item.field.related_query_name(),
                    Image.item.field.related_query_name(),
                ),
            )


class DetailItemTests(CheckFieldTestCase):
    fixtures = ["data.json"]

    def test_items_in_context(self):
        url = reverse("catalog:item-detail", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertIn("item", response.context)

    def test_items_size(self):
        url = reverse("catalog:item-detail", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertIsInstance(response.context["item"], Item)

    def test_items_loaded_values(self):
        url = reverse("catalog:item-detail", kwargs={"pk": 1})
        response = self.client.get(url)
        self.check_content_value(
            response.context["item"],
            (
                Item.name.field.name,
                Item.text.field.name,
                Item.category.field.attname,
            ),
            (Item.tags.field.name,),
            (
                Item.is_published.field.name,
                MainImage.item.field.related_query_name(),
                Image.item.field.related_query_name(),
            ),
        )
        self.check_content_value(
            response.context["item"].tags.all()[0],
            (Tag.name.field.name,),
            (),
            (),
        )


class CatalogFridayItemsTests(CheckFieldTestCase):
    fixtures = ["data.json"]

    def test_friday_items_in_context(self):
        response = self.client.get(reverse("catalog:friday-items"))
        self.assertIn("items", response.context)

    def test_friday_items_size(self):
        response = self.client.get(reverse("catalog:friday-items"))
        self.assertEqual(len(response.context["items"]), 0)

    def test_friday_items_types(self):
        response = self.client.get(reverse("catalog:friday-items"))
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
        response = self.client.get(reverse("catalog:friday-items"))
        for item in response.context["items"]:
            self.check_content_value(
                item,
                (
                    Item.name.field.name,
                    Item.text.field.name,
                    Item.category.field.attname,
                ),
                (Item.tags.field.name,),
                (
                    Item.is_published.field.name,
                    MainImage.item.field.related_query_name(),
                    Image.item.field.related_query_name(),
                ),
            )


class CatalogNewItemsTests(CheckFieldTestCase):
    fixtures = ["data.json"]

    def test_new_items_in_context(self):
        response = self.client.get(reverse("catalog:new-items"))
        self.assertIn("items", response.context)

    def test_new_items_size(self):
        response = self.client.get(reverse("catalog:new-items"))
        self.assertEqual(len(response.context["items"]), 0)

    def test_new_items_types(self):
        response = self.client.get(reverse("catalog:new-items"))
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
        response = self.client.get(reverse("catalog:new-items"))
        for item in response.context["items"]:
            self.check_content_value(
                item,
                (
                    Item.name.field.name,
                    Item.text.field.name,
                    Item.category.field.attname,
                ),
                (Item.tags.field.name,),
                (
                    Item.is_published.field.name,
                    MainImage.item.field.related_query_name(),
                    Image.item.field.related_query_name(),
                ),
            )


class CatalogUnverifiedNewItemsTests(CheckFieldTestCase):
    fixtures = ["data.json"]

    def test_unverified_items_in_context(self):
        response = self.client.get(reverse("catalog:unverified-items"))
        self.assertIn("items", response.context)

    def test_unverified_items_size(self):
        response = self.client.get(reverse("catalog:unverified-items"))
        self.assertEqual(len(response.context["items"]), 4)

    def test_unverified_items_types(self):
        response = self.client.get(reverse("catalog:unverified-items"))
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
        response = self.client.get(reverse("catalog:unverified-items"))
        for item in response.context["items"]:
            self.check_content_value(
                item,
                (
                    Item.name.field.name,
                    Item.text.field.name,
                    Item.category.field.attname,
                ),
                (Item.tags.field.name,),
                (
                    Item.is_published.field.name,
                    MainImage.item.field.related_query_name(),
                    Image.item.field.related_query_name(),
                ),
            )
