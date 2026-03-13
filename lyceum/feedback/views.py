__all__ = ()

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from feedback.forms import FeedbackForm


def feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            fb = form.save()

            send_mail(
                subject="Feedback Message",
                message=fb.text,
                from_email=settings.DJANGO_MAIL,
                recipient_list=[fb.mail],
                fail_silently=False,
            )

            messages.success(request, "Спасибо за отзыв!")
            return redirect("feedback:feedback")
    else:
        form = FeedbackForm()

    return render(request, "feedback/feedback.html", {"form": form})
