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
    post_data = request.POST if request.method == "POST" else None
    files_data = request.FILES if request.method == "POST" else None
    form_author = PersonalDataForm(post_data)
    form_content = FeedbackContentForm(post_data)
    form_files = FeedbackFileForm(post_data, files_data)
    if request.method == "POST":
        if (
            form_author.is_valid()
            and form_content.is_valid()
            and form_files.is_valid()
        ):
            personal_data_obj = form_author.save()

            feedback_obj = form_content.save(commit=False)
            feedback_obj.personal_data = personal_data_obj
            feedback_obj.save()
            files = request.FILES.getlist("files")
            for f in files:
                FeedbackFile.objects.create(feedback=feedback_obj, file=f)

            send_mail(
                subject="Feedback Message",
                message=form_content.cleaned_data["text"],
                from_email=settings.DJANGO_MAIL,
                recipient_list=[form_author.cleaned_data["mail"]],
                fail_silently=False,
            )

            messages.success(request, "Спасибо за отзыв!")
            return redirect("feedback:feedback")

    context = {
        "form_author": form_author,
        "form_content": form_content,
        "form_files": form_files,
    }

    return render(request, "feedback/feedback.html", context)
