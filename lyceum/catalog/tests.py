__all__ = []

from http import HTTPStatus

from django.core.exceptions import ValidationError
from django.test import Client, TestCase
import parameterized

from catalog.models import Category, Item, Tag


class StaticURLTests(TestCase):
    fixtures = ["new_data.json"]

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


class ModelsTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test category",
            slug="test-category",
        )
        self.tag = Tag.objects.create(name="Test tag", slug="test-tag")

        super(ModelsTests, self).setUp()

    def tearDown(self):
        Item.objects.all().delete()
        Tag.objects.all().delete()
        Category.objects.all().delete()

        super(ModelsTests, self).tearDown()

    @parameterized.parameterized.expand(
        [
            ("Превосходно"),
            ("роскошно"),
            ("роскошно!"),
            ("роскошно⌁"),
            ("!роскошно"),
            ("не роскошно"),
        ],
    )
    def test_item_validator(self, text):
        items_count = Item.objects.count()

        item = Item(
            name="Тестовый товар",
            text=text,
            category=self.category,
        )
        item.full_clean()
        item.save()
        item.tags.add(self.tag)

        self.assertEqual(
            Item.objects.count(),
            items_count + 1,
        )

    @parameterized.parameterized.expand(
        [
            ("Превос!ходно"),
            ("роскошный"),
            ("роскошноe"),
            ("рскошно⌁"),
            ("!ро скошно"),
            ("не рoскошно"),
        ],
    )
    def test_item_negative_validator(self, text):
        items_count = Item.objects.count()
        with self.assertRaises(ValidationError):
            item = Item(
                name="Тестовый товар",
                text=text,
                category=self.category,
            )
            item.full_clean()
            item.save()
            item.tags.add(self.tag)

        self.assertEqual(
            Item.objects.count(),
            items_count,
        )

    @parameterized.parameterized.expand(
        [
            (1),
            (100),
            (32000),
        ],
    )
    def test_category_validator(self, weight):
        categories_count = Category.objects.count()

        test_category = Category(
            name="Тестовая категория",
            weight=weight,
            slug="test-cat",
        )
        test_category.full_clean()
        test_category.save()

        self.assertEqual(
            Category.objects.count(),
            categories_count + 1,
        )

    @parameterized.parameterized.expand(
        [
            (-100),
            (0),
            (64000),
        ],
    )
    def test_category_negative_validator(self, weight):
        categories_count = Category.objects.count()

        with self.assertRaises(ValidationError):
            test_category = Category(
                name="Тестовая категория",
                weight=weight,
                slug="test-cat",
            )
            test_category.full_clean()
            test_category.save()

        self.assertEqual(
            Category.objects.count(),
            categories_count,
        )

    def test_normalized_category_negative(self):
        categories_count = Category.objects.count()
        try:
            test_category_1 = Category(
                name="test_123$$",
                weight=100,
                slug="test-cat",
            )
            test_category_2 = Category(
                name="test_123",
                weight=100,
                slug="test-cat-real",
            )
            test_category_1.full_clean()
            test_category_1.save()
            test_category_2.full_clean()
            test_category_2.save()
        except Exception:
            self.assertEqual(
                Category.objects.count(),
                categories_count + 1,
            )

    def test_normalized_category_positive(self):
        categories_count = Category.objects.count()

        test_category_1 = Category(
            name="test_123$$",
            weight=100,
            slug="test-cat",
        )
        test_category_2 = Category(
            name="test_12$$",
            weight=100,
            slug="test-cat-real",
        )
        test_category_1.full_clean()
        test_category_1.save()
        test_category_2.full_clean()
        test_category_2.save()

        self.assertEqual(
            Category.objects.count(),
            categories_count + 2,
        )

    def test_normalized_tag_negative(self):
        tags_count = Tag.objects.count()
        try:
            test_tag_1 = Tag(
                name="test_12345$$",
                slug="test-catik",
            )
            test_tag_2 = Tag(
                name="test_12345",
                slug="test-catik-real",
            )
            test_tag_1.full_clean()
            test_tag_1.save()
            test_tag_2.full_clean()
            test_tag_2.save()
        except Exception:
            self.assertEqual(
                Tag.objects.count(),
                tags_count + 1,
            )

    def test_normalized_tag_positive(self):
        tags_count = Tag.objects.count()

        test_tag_1 = Tag(
            name="test_123$$",
            slug="test-cat",
        )
        test_tag_2 = Tag(
            name="test_12$$",
            slug="test-cat-real",
        )
        test_tag_1.full_clean()
        test_tag_1.save()
        test_tag_2.full_clean()
        test_tag_2.save()
        self.assertEqual(
            Tag.objects.count(),
            tags_count + 2,
        )


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
    fixtures = ["new_data.json"]

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
    fixtures = ["new_data.json"]

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
