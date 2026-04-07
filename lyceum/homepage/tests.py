__all__ = ()

from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from catalog.models import Item
from core.tests import CheckFieldTestCase
from users.models import Profile

User = get_user_model()


class StaticURLTests(TestCase):
    def test_homepage_endpoint(self):
        response = Client().get(reverse("homepage:home"))
        self.assertEqual(response.status_code, HTTPStatus.OK)


class CoffeeViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
        )
        Profile.objects.create(user=self.user)
        self.client = Client()
        self.client.login(username="testuser", password="testpass123")

    def test_coffee_status_code(self):
        response = self.client.get(reverse("homepage:coffee"))
        self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)
        self.assertEqual(response.content.decode(), "Я чайник")


class HomepageItemsTests(CheckFieldTestCase):
    fixtures = ["data.json"]

    def test_items_in_context(self):
        response = self.client.get(reverse("homepage:home"))
        self.assertIn("items", response.context)

    def test_items_size(self):
        response = self.client.get(reverse("homepage:home"))
        self.assertEqual(len(response.context["items"]), 4)

    def test_items_types(self):
        response = self.client.get(reverse("homepage:home"))
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
        response = self.client.get(reverse("homepage:home"))
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
