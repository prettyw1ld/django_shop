__all__ = ()


from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import Profile, SignUpForm, User

user_ = get_user_model()


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
        user = user_.objects.get(username=username)
    except user_.DoesNotExist:
        return HttpResponse("Пользователь не найден", status=404)

    if timezone.now() - user.date_joined > timedelta(hours=12):
        return HttpResponse("Ссылка устарела", status=410)

    user.is_active = True
    user.save()
    return redirect("login")


def user_list(request):
    template = "users/user_list.html"
    users = (
        user_.objects.filter(is_active=True).prefetch_related("profile").all()
    )
    return render(request, template, {"users": users})


def user_detail(request, user_id):
    template = "users/user_detail.html"
    try:
        user = user_.objects.select_related("profile").get(
            id=user_id,
            is_active=True,
        )
    except user_.DoesNotExist:
        return HttpResponse("Пользователь не найден", status=404)

    return render(request, template, {"user": user})


@login_required
def profile(request):
    template = "users/profile.html"
    try:
        user = user_.objects.select_related("profile").get(
            id=request.user.id,
            is_active=True,
        )
    except user_.DoesNotExist:
        return HttpResponse("Пользователь не найден", status=404)

    profile = user.profile

    form_profile = Profile(
        request.POST or None,
        request.FILES,
        instance=profile,
    )
    form_user = User(request.POST or None, instance=user)

    if request.method == "POST":
        if form_profile.is_valid() and form_user.is_valid():
            form_profile.save()
            form_user.save()
            messages.success(request, "Профиль успешно обновлен!")
            return redirect("users:profile")

    return render(
        request,
        template,
        {
            "form_profile": form_profile,
            "form_user": form_user,
            "user": user,
        },
    )
