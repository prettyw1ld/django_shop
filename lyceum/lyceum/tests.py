__all__ = ()

import django.test

from lyceum.middleware import RUSSIAN_WORD_REGEX, WORDS_REGEX


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
