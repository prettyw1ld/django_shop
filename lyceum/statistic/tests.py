__all__ = ()

from http import HTTPStatus

import django.test

from catalog.models import Category, Item
from rating.models import Rating

User = django.contrib.auth.get_user_model()


class StatisticTests(django.test.TestCase):
    def setUp(self):
        self.damir = User.objects.create_user(
            username="damir",
            password="pass1234",
        )
        self.category = Category.objects.create(
            name="Тестовая категория",
            is_published=True,
        )
        self.item = Item.objects.create(
            name="Тестовый товар",
            is_published=True,
            category=self.category,
        )
        self.score = Rating.objects.create(
            user=self.damir,
            item=self.item,
            score=4,
        )
        self.user_url = django.urls.reverse(
            "statistic:statistic-user",
        )
        self.url = django.urls.reverse(
            "statistic:statistic-item-detail",
            kwargs={"pk": self.item.pk},
        )

    def test_statistic_user_view_anonymous(self):
        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn("/auth/login/?next=/statistic/", response.url)

    def test_statistic_user_view(self):
        self.client.force_login(self.damir)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_statistic_user_rating_count(self):
        self.client.force_login(self.damir)
        response = self.client.get(self.user_url)
        self.assertEqual(response.context["rating_count"], 1)

    def test_statistic_user_rating_avg(self):
        self.client.force_login(self.damir)
        response = self.client.get(self.user_url)
        self.assertAlmostEqual(float(response.context["rating_avg"]), 4.0)

    def test_statistic_user_best_item(self):
        self.client.force_login(self.damir)
        response = self.client.get(self.user_url)
        self.assertEqual(response.context["best_item"], self.item)

    def test_statistic_user_worst_item(self):
        self.client.force_login(self.damir)
        response = self.client.get(self.user_url)
        self.assertEqual(response.context["worst_item"], self.item)

    def test_statistic_user_items_contains_score(self):
        self.client.force_login(self.damir)
        response = self.client.get(self.user_url)
        items = response.context["items"]
        self.assertEqual(items[0].user_score, 4)

    def test_statistic_item_detail_ok(self):
        self.client.force_login(self.damir)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_statistic_item_detail_rating_count(self):
        self.client.force_login(self.damir)
        response = self.client.get(self.url)
        self.assertEqual(response.context["rating_count"], 1)

    def test_statistic_item_detail_rating_avg(self):
        self.client.force_login(self.damir)
        response = self.client.get(self.url)
        self.assertAlmostEqual(float(response.context["rating_avg"]), 4.0)

    def test_statistic_item_detail_last_max_user(self):
        self.client.force_login(self.damir)
        response = self.client.get(self.url)
        self.assertEqual(response.context["last_max_user"].user, self.damir)
