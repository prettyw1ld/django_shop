import django.test


class StaticURLTests(django.test.TestCase):
    def test_catalog_endpoint(self):
        response = django.test.Client().get("/")
        self.assertEqual(response.status_code, 200)
