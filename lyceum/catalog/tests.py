from http import HTTPStatus

from django.core.exceptions import ValidationError
from django.test import Client, TestCase
import parameterized

from catalog.models import Category, Item, Tag


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
        ],
    )
    def test_catalog_item_endpoint(self, url, expected_status):
        response = Client().get(f"/catalog/{url}/")
        self.assertEqual(response.status_code, expected_status)

    @parameterized.parameterized.expand(
        [
            (prefix, url, expected_status)
            for prefix in ["converter", "re"]
            for url, expected_status in [
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
            ]
        ],
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


class TestModel(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = Category.objects.create(
            is_published=True,
            name="Тестовая категория",
            slug="test-category-slug",
            weight=100,
        )
        cls.tag = Tag.objects.create(
            is_published=True,
            name="Тестовый тэг",
            slug="test-tug-slug",
        )

    def test_unable_create_one_letter(self):
        item_count = Item.objects.count()
        with self.assertRaises(ValidationError):
            self.item = Item(
                name="Тестовый товар",
                category=self.category,
                text="1",
            )
            self.item.full_clean()
            self.item.save()
            self.item.tags.add(TestModel.tag)
        self.assertEqual(Item.objects.count(), item_count)

    def test_able_create_one_letter(self):
        item_count = Item.objects.count()
        self.item = Item(
            name="Тестовый товар",
            category=self.category,
            text="123 превосходно",
        )
        self.item.full_clean()
        self.item.save()
        self.item.tags.add(TestModel.tag)
        self.assertEqual(Item.objects.count(), item_count + 1)
