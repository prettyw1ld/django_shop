__all__ = ()

from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import SignUpForm

User = get_user_model()


def signup_view(request):
    template = "users/signup.html"
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = settings.DEFAULT_USER_IS_ACTIVE
            user.is_staff = False
            user.is_superuser = False
            user.save()

            activation_link = request.build_absolute_uri(
                f"/activate/{user.username}/",
            )
            send_mail(
                subject="Подтверждение регистрации",
                message=f"Для активации аккаунта перейдите по ссылке:\n"
                f"{activation_link}\n\nСсылка действительна 12 часов.",
                from_email=settings.DJANGO_MAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            return redirect("homepage:home")
    else:
        form = SignUpForm()

    return render(request, template, {"form": form})


def activate_view(request, username):
    user = get_user_model()
    try:
        user = user.objects.get(username=username)
    except user.DoesNotExist:
        return HttpResponse("Пользователь не найден", status=404)

    if timezone.now() - user.date_joined > timedelta(hours=12):
        return HttpResponse("Ссылка устарела", status=410)

    user.is_active = True
    user.save()
    return redirect("login")


def user_list(request):
    template = "users/user_list.html"
    users = (
        User.objects.filter(is_active=True).prefetch_related("profile").all()
    )
    return render(request, template, {"users": users})


def user_detail(request, user_id):
    template = "users/user_detail.html"
    try:
        user = User.objects.select_related("profile").get(
            id=user_id,
            is_active=True,
        )
    except User.DoesNotExist:
        return HttpResponse("Пользователь не найден", status=404)

    return render(request, template, {"user": user})
