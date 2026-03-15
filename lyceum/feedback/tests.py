__all__ = ()

from django.core.files.uploadedfile import SimpleUploadedFile
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

    def test_invalid_email_error(self):
        form_data = {
            "name": "Ivan",
            "text": "Hello",
            "mail": "not-an-email",
        }
        form = feedback.forms.FeedbackForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("mail", form.errors)

    def test_unable_create_feedback(self):
        item_count = feedback.models.Feedback.objects.count()
        form_data = {
            "name": "Test",
            "text": "Test",
            "mail": "Test",
        }
        response = self.client.post(
            django.urls.reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )
        self.assertTrue(response.context["form"].has_error("mail"))
        self.assertEqual(
            feedback.models.Feedback.objects.count(),
            item_count,
        )


class FeedbackFileTests(TestCase):
    def test_file_upload_and_db_structure(self):
        file1 = SimpleUploadedFile("test_file1.txt", b"content1")
        file2 = SimpleUploadedFile("test_file2.txt", b"content2")

        form_data = {
            "name": "Тестер",
            "mail": "test@example.com",
            "text": "Проверка загрузки файлов",
            "files": [file1, file2],
        }

        response = self.client.post(
            django.urls.reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            feedback.models.FeedbackPersonalData.objects.count(),
            1,
        )
        self.assertEqual(feedback.models.Feedback.objects.count(), 1)

        fb = feedback.models.Feedback.objects.first()
        personal = feedback.models.FeedbackPersonalData.objects.first()

        self.assertEqual(fb.personal_data, personal)
        self.assertEqual(personal.mail, "test@example.com")

        self.assertEqual(fb.files.count(), 2)

        first_file = fb.files.first()
        expected_path_part = f"uploads/{fb.id}/"
        self.assertTrue(first_file.file.name.startswith(expected_path_part))
