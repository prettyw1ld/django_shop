__all__ = ()

from datetime import timedelta
from unittest.mock import patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from users.models import Profile

User = get_user_model()


class SignupActivationTest(TestCase):
    def setUp(self):
        self.client = Client()

    @patch("django.core.mail.send_mail")
    def test_signup_creates_inactive_user(self, mock_mail):
        with self.settings(DEFAULT_USER_IS_ACTIVE=False):
            self.client.post(
                reverse("users:signup"),
                {
                    "username": "testuser",
                    "password1": "StrongPass123!",
                    "password2": "StrongPass123!",
                    "email": "test@test.com",
                },
            )
            user = User.objects.get(username="testuser")
            self.assertFalse(user.is_active)

    @patch("django.core.mail.send_mail")
    def test_activation_link_works(self, mock_mail):
        self.client.post(
            reverse("users:signup"),
            {
                "username": "testuser",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
                "email": "test@test.com",
            },
        )
        self.client.post(reverse("users:activate", kwargs={"pk": 1}))
        user = User.objects.get(username="testuser")
        self.assertTrue(user.is_active)

    @patch("django.core.mail.send_mail")
    def test_activation_link_expired(self, mock_mail):
        with self.settings(DEFAULT_USER_IS_ACTIVE=False):
            self.client.post(
                reverse("users:signup"),
                {
                    "username": "testuser",
                    "password1": "StrongPass123!",
                    "password2": "StrongPass123!",
                    "email": "test@test.com",
                },
            )
            user = User.objects.get(username="testuser")
            user.date_joined = timezone.now() - timedelta(hours=13)
            user.save()

            response = self.client.get(
                reverse("users:activate", kwargs={"pk": 1}),
            )
            self.assertEqual(response.status_code, 302)
            user.refresh_from_db()
            self.assertFalse(user.is_active)


class LoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="StrongPass123!",
            email="damirka228@yandex.ru",
            is_active=True,
        )
        Profile.objects.create(user=self.user)

    def test_username_login(self):
        response = self.client.post(
            reverse("users:login"),
            {
                "username": "testuser",
                "password": "StrongPass123!",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("users:profile"), response.url)

    def test_email_login(self):
        response = self.client.post(
            reverse("users:login"),
            {
                "username": "damirka228@yandex.ru",
                "password": "StrongPass123!",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("users:profile"), response.url)

    def test_blocked_login(self):
        for _ in range(settings.MAX_AUTH_ATTEMPTS):
            self.client.post(
                reverse("users:login"),
                {
                    "username": "testuser",
                    "password": "WrongPass123!",
                },
            )

        response = self.client.post(
            reverse("users:login"),
            {
                "username": "testuser",
                "password": "StrongPass123!",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Эта учетная запись отключена.",
        )
