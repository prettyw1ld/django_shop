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
    author = PersonalDataForm()
    content = FeedbackContentForm()
    files = FeedbackFileForm()

    if request.method == "POST" or None:
        author = PersonalDataForm(request.POST)
        content = FeedbackContentForm(request.POST)
        files = FeedbackFileForm(request.POST, request.FILES)
        if author.is_valid() and content.is_valid() and files.is_valid():
            personal_data = author.save()
            feedback = content.save(commit=False)
            feedback.personal_data = personal_data
            feedback.save()
            for f in request.FILES.getlist("files"):
                FeedbackFile.objects.create(feedback=feedback, file=f)

            send_mail(
                subject="Feedback Message",
                message=content.cleaned_data["text"],
                from_email=settings.DJANGO_MAIL,
                recipient_list=[author.cleaned_data["mail"]],
                fail_silently=False,
            )

            messages.success(request, "Спасибо за отзыв!")
            return redirect("feedback:feedback")

    context = {
        "author": author,
        "content": content,
        "files": files,
    }

    return render(request, "feedback/feedback.html", context)
