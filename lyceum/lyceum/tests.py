__all__ = []

import django.test
from django.urls import reverse

from lyceum.middleware import RUSSIAN_WORD_REGEX


class RussianReverseTest(django.test.TestCase):
    def reverse_russian_words(self, text):
        def replace_func(match):
            word = match.group()
            return word[::-1]

        return RUSSIAN_WORD_REGEX.sub(replace_func, text)

    @django.test.override_settings(ALLOW_REVERSE=True)
    def test_reverse_russian_words_enabled(self):
        contents = {
            django.test.Client().get(reverse("homepage:coffee")).content
            for _ in range(10)
        }
        self.assertIn("Я чайник".encode(), contents)
        self.assertIn("Я кинйач".encode(), contents)

    @django.test.override_settings(ALLOW_REVERSE=False)
    def test_reverse_russian_words_disabled(self):
        contents = {
            django.test.Client().get(reverse("homepage:coffee")).content
            for _ in range(10)
        }
        self.assertIn("Я чайник".encode(), contents)
        self.assertNotIn("Я кинйач".encode(), contents)

    def test_reverse_russian_words_default(self):
        contents = {
            django.test.Client().get(reverse("homepage:coffee")).content
            for _ in range(10)
        }
        self.assertIn("Я чайник".encode(), contents)
        self.assertIn("Я кинйач".encode(), contents)

    def test_reverse_russian_words_every_twenty(self):
        contents = {
            django.test.Client().get(reverse("homepage:coffee")).content
            for _ in range(20)
        }
        self.assertIn("Я чайник".encode(), contents)
        self.assertIn("Я кинйач".encode(), contents)

    def test_mixed_reverse(self):
        test_cases = [
            ("Hello привет World мир", "Hello тевирп World рим"),
            ("Meowmeow2мяумяуMeoewMeow123", "Meowmeow2уямуямMeoewMeow123"),
            (
                "Русский english смешанный text",
                "йикссуР english йыннашемс text",
            ),
            ("abcдефghi", "abcфедghi"),
        ]

        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                self.assertEqual(
                    self.reverse_russian_words(input_text),
                    expected,
                )
