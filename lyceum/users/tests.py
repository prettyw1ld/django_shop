__all__ = ()

from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

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
        self.client.get(reverse("users:activate", args=["testuser"]))
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
                reverse("users:activate", args=["testuser"]),
            )
            self.assertEqual(response.status_code, 410)
            user.refresh_from_db()
            self.assertFalse(user.is_active)
