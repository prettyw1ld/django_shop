import django.test

__all__ = []


class RussianReverseTest(django.test.TestCase):
    @django.test.override_settings(ALLOW_REVERSE=True)
    def test_reverse_russian_words_enabled(self):
        contents = {
            django.test.Client().get("/coffee/").content for _ in range(10)
        }
        self.assertIn("Я чайник".encode(), contents)
        self.assertIn("Я кинйач".encode(), contents)

    @django.test.override_settings(ALLOW_REVERSE=False)
    def test_reverse_russian_words_disabled(self):
        contents = {
            django.test.Client().get("/coffee/").content for _ in range(10)
        }
        self.assertIn("Я чайник".encode(), contents)
        self.assertNotIn("Я кинйач".encode(), contents)
