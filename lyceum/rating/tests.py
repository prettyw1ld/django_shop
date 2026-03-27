__all__ = ()

import django.contrib.auth
import django.test
import django.urls

from catalog.models import Category, Item
from rating.models import Rating

User = django.contrib.auth.get_user_model()


class RatingTests(django.test.TestCase):

    def setUp(self):
        self.damir = User.objects.create_user(
            username="damir",
            password="pass1234",
        )
        self.denik = User.objects.create_user(
            username="denik",
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
        self.url = django.urls.reverse(
            "catalog:item-detail",
            kwargs={"pk": self.item.pk},
        )

    def test_can_rate_item(self):
        self.client.force_login(self.damir)
        self.client.post(self.url, {"score": 5})
        self.assertTrue(
            Rating.objects.filter(user=self.damir, item=self.item).exists(),
        )

    def test_anonymous_cannot_rate(self):
        self.client.post(self.url, {"score": 5})
        self.assertFalse(Rating.objects.exists())

    def test_update_rating(self):
        Rating.objects.create(user=self.damir, item=self.item, score=1)
        self.client.force_login(self.damir)
        self.client.post(self.url, {"score": 5})
        rating = Rating.objects.get(user=self.damir, item=self.item)
        self.assertEqual(rating.score, 5)

    def test_delete_rating_via_empty_score(self):
        Rating.objects.create(user=self.damir, item=self.item, score=3)
        self.client.force_login(self.damir)
        self.client.post(self.url, {"score": ""})
        self.assertFalse(
            Rating.objects.filter(user=self.damir, item=self.item).exists(),
        )

    def test_delete_rating_via_button(self):
        Rating.objects.create(user=self.damir, item=self.item, score=3)
        self.client.force_login(self.damir)
        self.client.post(self.url, {"delete": "1"})
        self.assertFalse(
            Rating.objects.filter(user=self.damir, item=self.item).exists(),
        )

    def test_empty_score_without_existing_rating_does_nothing(self):
        self.client.force_login(self.damir)
        self.client.post(self.url, {"score": ""})
        self.assertFalse(Rating.objects.exists())

    def test_separate_ratings(self):
        Rating.objects.create(user=self.damir, item=self.item, score=5)
        Rating.objects.create(user=self.denik, item=self.item, score=1)
        self.assertEqual(Rating.objects.count(), 2)

    def test_duplicate_rating_raises_error(self):
        Rating.objects.create(user=self.damir, item=self.item, score=5)
        with self.assertRaises(Exception):
            Rating.objects.create(user=self.damir, item=self.item, score=3)

    def test_count_and_avg_in_context(self):
        Rating.objects.create(user=self.damir, item=self.item, score=5)
        Rating.objects.create(user=self.denik, item=self.item, score=3)
        self.client.force_login(self.damir)
        response = self.client.get(self.url)
        self.assertEqual(response.context["rating_count"], 2)
        self.assertAlmostEqual(response.context["rating_avg"], 4.0)
