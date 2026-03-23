__all__ = ()


from datetime import timedelta

from django.conf import settings
from django.contrib import messages
import django.contrib.auth
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
import django.urls
from django.utils import timezone

from users.forms import UpdateProfileForm, UserChangeForm, UserCreationForm
import users.models


def signup_view(request):
    form = UserCreationForm(request.POST or None)
    context = {"form": form}
    template = "users/signup.html"

    if request.method == "POST" and form.is_valid():
        user = form.save()
        user.is_active = settings.DEFAULT_USER_IS_ACTIVE
        user.save()
        profile = users.models.Profile.objects.create(user=user)
        profile.save()

        activation_link = (
            django.urls.reverse("users:activate", kwargs={"pk": user.id}),
        )
        send_mail(
            subject="Подтверждение регистрации",
            message=f"Для активации аккаунта перейдите по ссылке:\n"
            f"{activation_link}\n\nСсылка действительна 12 часов.",
            from_email=settings.DJANGO_MAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return redirect(django.urls.reverse("homepage:home"))

    return render(request, template, context)


def activate_view(request, pk):
    user = get_object_or_404(users.models.User, pk=pk)
    if not user.is_active and timezone.now() - user.date_joined <= timedelta(
        hours=12
    ):
        user.is_active = True
        user.save()

    return redirect(django.urls.reverse("homepage:home"))


def reactivate_view(request, pk):
    user = users.models.User.objects.get(pk=pk)
    if (
        user.profile.block_date is not None
        and user.profile.block_date + timedelta(hours=7) > timezone.now()
    ):
        user.is_active = True
        user.save()

    return redirect(django.urls.reverse("homepage:home"))


def user_list(request):
    context = {"users": users.models.User.objects.active()}
    template = "users/user_list.html"
    return render(request, template, context)


def user_detail(request, pk: int):
    search_user = get_object_or_404(
        users.models.User.objects.active(),
        pk=pk,
    )
    context = {"user": search_user}
    template = "users/user_detail.html"

    return render(request, template, context)


@login_required
def profile(request):
    template = "users/profile.html"
    user_form = UserChangeForm(
        request.POST or None,
        instance=request.user,
    )
    profile_form = UpdateProfileForm(
        request.POST or None,
        instance=request.user.profile,
    )
    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }

    if (
        request.method == "POST"
        and user_form.is_valid()
        and profile_form.is_valid()
    ):
        user_form.save()
        profile_form.save()
        messages.success(request, "Профиль успешно обновлен")
        return redirect(django.urls.reverse("users:profile"))

    return render(request, template, context)
