__all__ = ()

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from feedback.forms import (
    FeedbackContentForm,
    FeedbackFileForm,
    PersonalDataForm,
)
from feedback.models import FeedbackFile


def feedback(request):
    template = "feedback/feedback.html"
    author_form = PersonalDataForm()
    content_form = FeedbackContentForm()
    files_form = FeedbackFileForm()

    if request.method == "POST":
        author_form = PersonalDataForm(request.POST or None)
        content_form = FeedbackContentForm(request.POST or None)
        files_form = FeedbackFileForm(request.POST or None, request.FILES)
        if (
            author_form.is_valid()
            and content_form.is_valid()
            and files_form.is_valid()
        ):
            personal_data = author_form.save()
            feedback = content_form.save(commit=False)
            feedback.personal_data = personal_data
            feedback.save()
            for f in request.FILES.getlist("files"):
                FeedbackFile.objects.create(feedback=feedback, file=f)

            send_mail(
                subject="Feedback Message",
                message=content_form.cleaned_data["text"],
                from_email=settings.DJANGO_MAIL,
                recipient_list=[author_form.cleaned_data["mail"]],
                fail_silently=False,
            )

            messages.success(request, "Спасибо за отзыв!")
            return redirect("feedback:feedback")

    context = {
        "author": author_form,
        "content": content_form,
        "files": files_form,
    }

    return render(request, template, context)
