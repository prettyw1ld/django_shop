__all__ = ()

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from feedback.forms import FeedbackForm
from feedback.models import Feedback, FeedbackFile, FeedbackPersonalData


def feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            personal_data = FeedbackPersonalData.objects.create(
                name=cleaned_data["name"],
                mail=cleaned_data["mail"],
            )
            feedback_obj = Feedback.objects.create(
                personal_data=personal_data,
                text=cleaned_data["text"],
            )
            files = request.FILES.getlist("files")
            for f in files:
                FeedbackFile.objects.create(feedback=feedback_obj, file=f)

            send_mail(
                subject="Feedback Message",
                message=cleaned_data["text"],
                from_email=settings.DJANGO_MAIL,
                recipient_list=[cleaned_data["mail"]],
                fail_silently=False,
            )

            messages.success(request, "Спасибо за отзыв!")
            return redirect("feedback:feedback")
    else:
        form = FeedbackForm()

    return render(request, "feedback/feedback.html", {"form": form})
