__all__ = ()

import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, override_settings, TestCase
from django.urls import reverse

import feedback.forms
from feedback.models import Feedback


@override_settings(
    MEDIA_ROOT=tempfile.TemporaryDirectory().name,
)
class FeedbackTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = feedback.forms.FeedbackContentForm()
        cls.files_form = feedback.forms.FeedbackFileForm()
        cls.author_form = feedback.forms.PersonalDataForm()

    def test_file_upload_creation(self):
        unique_text = "Unique feedback text 12345"
        response = self.client.post(
            reverse("feedback:feedback"),
            data={
                "name": "Test",
                "mail": "popik@test.com",
                "text": unique_text,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Feedback.objects.filter(text=unique_text).exists())

    def test_files_count_after_upload(self):
        file1 = SimpleUploadedFile("test1.txt", b"content1")
        file2 = SimpleUploadedFile("test2.txt", b"content2")
        response = self.client.post(
            reverse("feedback:feedback"),
            data={
                "name": "Test",
                "mail": "denik@test.com",
                "text": "File test",
                "files": [file1, file2],
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

        feedback_obj = Feedback.objects.get(text="File test")
        self.assertEqual(feedback_obj.files.count(), 2)

    def test_upload_path_structure(self):
        file = SimpleUploadedFile("my_file.txt", b"content")
        self.client.post(
            reverse("feedback:feedback"),
            data={
                "name": "Test",
                "mail": "domir@test.com",
                "text": "Path test",
                "files": [file],
            },
        )
        feedback_obj = Feedback.objects.get(text="Path test")
        file_obj = feedback_obj.files.first()
        self.assertIn(f"uploads/{feedback_obj.id}/", file_obj.file.name)

    def test_name_label(self):
        name_label = self.author_form.fields["name"].label
        self.assertEqual(name_label, "Имя")

    def test_help_text(self):
        name_help_text = self.author_form.fields["name"].help_text
        self.assertEqual(name_help_text, "Введите ваше имя")

    def test_unable_create_feedback(self):
        item_count = Feedback.objects.count()
        form_data = {
            "name": "Test",
            "mail": "testtest.com",
            "text": "Path test",
        }

        response = Client().post(
            reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )
        self.assertTrue(response.context["form"].has_error("mail"))
        self.assertEqual(
            Feedback.objects.count(),
            item_count,
        )
