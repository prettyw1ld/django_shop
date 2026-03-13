__all__ = ()

from django.core.exceptions import ValidationError
from django.test import Client, TestCase
import django.urls

import feedback.forms
import feedback.models


class FormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = feedback.forms.FeedbackForm()

    def test_name_label(self):
        name_label = FormTests.form.fields["name"].label
        self.assertEqual(name_label, "Имя")

    def test_text_label(self):
        name_label = FormTests.form.fields["text"].label
        self.assertEqual(name_label, "Обратная связь")

    def test_mail_label(self):
        name_label = FormTests.form.fields["mail"].label
        self.assertEqual(name_label, "Почта")

    def test_text_help_text(self):
        name_label = FormTests.form.fields["text"].help_text
        self.assertEqual(
            name_label,
            "Напишите в этом поле все то,"
            " что хотели бы сказать разработчикам",
        )

    def test_mail_help_text(self):
        name_label = FormTests.form.fields["mail"].help_text
        self.assertEqual(name_label, "max 150 символов")

    def test_create_task(self):
        form_data = {
            "name": "Зульфия",
            "text": "Ну ничо такой сайтик да",
            "mail": "zulfiya@gmail.com",
        }

        response = Client().post(
            django.urls.reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response,
            django.urls.reverse("feedback:feedback"),
        )


class TestModel(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_unable_create_one_feedback(self):
        items_count = feedback.models.Feedback.objects.count()
        with self.assertRaises(ValidationError):
            self.form = feedback.models.Feedback(
                name="Зульфия",
                text="Ну ничо такой сайтик да",
                mail="zulfiyagmail.com",
            )
            self.form.full_clean()
            self.form.save()

        self.assertEqual(items_count, items_count)

    def test_able_create_one_feedback(self):
        items_count = feedback.models.Feedback.objects.count()
        self.form = feedback.models.Feedback(
            name="Зульфия",
            text="Ну ничо такой сайтик да",
            mail="zulfiya@gmail.com",
        )
        self.form.full_clean()
        self.form.save()
        self.assertEqual(
            feedback.models.Feedback.objects.count(),
            items_count + 1,
        )

    def test_feedback_creates_db_entry(self):
        form_data = {
            "name": "Ivan",
            "text": "Тестовый текст",
            "mail": "test@example.com",
        }
        response = self.client.post(
            django.urls.reverse("feedback:feedback"),
            data=form_data,
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(feedback.models.Feedback.objects.count(), 1)

        fb = feedback.models.Feedback.objects.first()
        self.assertEqual(fb.name, "Ivan")
        self.assertEqual(fb.status, "received")

    def test_invalid_email_error(self):
        form_data = {
            "name": "Ivan",
            "text": "Hello",
            "mail": "not-an-email",
        }
        form = feedback.forms.FeedbackForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("mail", form.errors)
