__all__ = []

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from feedback.forms import FeedbackForm


def feedback(request):
    template = "feedback/feedback.html"
    form = FeedbackForm(request.POST or None)

    if form.is_valid():
        name = form.cleaned_data.get("name")
        text = form.cleaned_data.get("text")
        mail = form.cleaned_data.get("mail")

        full_message = f"Привет, {name}!\n\nТекст отправителя: {text}"

        send_mail(
            subject="Обратная связь",
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[mail],
        )

        messages.success(request, "Форма успешно отправлена!")
        return redirect("feedback:feedback")

    context = {
        "form": form,
    }
    return render(request, template, context)
