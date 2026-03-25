__all__ = ()

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect
import django.views.generic

from feedback.forms import (
    FeedbackContentForm,
    FeedbackFileForm,
    PersonalDataForm,
)
from feedback.models import FeedbackFile


class FeedbackView(django.views.generic.View):
    template_name = "feedback/feedback.html"

    def get_forms(self, data=None, files=None):
        return {
            "author": PersonalDataForm(data),
            "content": FeedbackContentForm(data),
            "files": FeedbackFileForm(data, files),
        }

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_forms())

    def post(self, request, *args, **kwargs):
        forms = self.get_forms(request.POST, request.FILES)

        if all(form.is_valid() for form in forms.values()):
            return self.forms_valid(forms)

        return self.forms_invalid(forms)

    def forms_valid(self, forms):
        personal_data = forms["author"].save()
        feedback = forms["content"].save(commit=False)
        feedback.personal_data = personal_data
        feedback.save()

        for f in self.request.FILES.getlist("files"):
            FeedbackFile.objects.create(feedback=feedback, file=f)

        send_mail(
            subject="Feedback Message",
            message=forms["content"].cleaned_data["text"],
            from_email=settings.DJANGO_MAIL,
            recipient_list=[forms["author"].cleaned_data["mail"]],
            fail_silently=False,
        )

        messages.success(self.request, "Спасибо за отзыв!")
        return redirect("feedback:feedback")

    def forms_invalid(self, forms):
        return self.render_to_response(forms)
