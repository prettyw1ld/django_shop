__all__ = ()

import django.test
from django.urls import reverse
import django.utils.timezone

from lyceum.middleware import RUSSIAN_WORD_REGEX, WORDS_REGEX
from users.models import Profile, User


class RussianReverseTest(django.test.TestCase):
    def reverse_russian_words(self, text):
        words = WORDS_REGEX.findall(text)
        transformed = [
            word[::-1] if RUSSIAN_WORD_REGEX.search(word) else word
            for word in words
        ]
        return "".join(transformed)

    @django.test.override_settings(ALLOW_REVERSE=True)
    def test_mixed_reverse(self):
        test_cases = [
            ("Hello привет World мир", "Hello тевирп World рим"),
            ("Meowmeow2мяумяуMeoewMeow123", "Meowmeow2мяумяуMeoewMeow123"),
            (
                "Русский english смешанный text",
                "йикссуР english йыннашемс text",
            ),
            ("abcдефghi", "abcдефghi"),
        ]

        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                self.assertEqual(
                    self.reverse_russian_words(input_text),
                    expected,
                )


class ContextProcessorsTest(django.test.TestCase):
    def test_birthdays_positive(self):
        user = User.objects.create(
            username="testuser",
            email="testuser@example.com",
            first_name="Олег",
            is_active=True,
        )
        profile = Profile.objects.create(user=user)
        today = django.utils.timezone.localdate()
        profile.birthday = today
        profile.save()
        url = reverse("homepage:home")
        response = self.client.get(url)
        birthdays_users = response.context["birthdays_users"]
        self.assertIn(
            {
                "first_name": "Олег",
                "email": "testuser@example.com",
            },
            birthdays_users,
        )

    def test_birthdays_negative(self):
        user = User.objects.create(
            username="testuser",
            email="testuser@example.com",
            first_name="Олег",
            is_active=False,
        )
        profile = Profile.objects.create(user=user)
        today = django.utils.timezone.localdate()
        profile.birthday = today
        user.save()
        profile.save()
        url = reverse("homepage:home")
        response = self.client.get(url)
        birthdays_users = response.context["birthdays_users"]
        self.assertNotIn(
            {
                "first_name": "Олег",
                "email": "testuser@example.com",
                "profile__birthday": today,
            },
            birthdays_users,
        )
