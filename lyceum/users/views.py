__all__ = ()


from datetime import timedelta

from django.conf import settings
from django.contrib import messages
import django.contrib.auth.mixins
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
import django.urls
from django.utils import timezone
import django.views.generic

from users.forms import UpdateProfileForm, UserChangeForm, UserCreationForm
import users.models


class SignUpView(django.views.generic.FormView):
    template_name = "users/signup.html"
    form_class = UserCreationForm

    def form_valid(self, form):
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


class ActivateView(django.views.generic.View):
    def get(self, request, pk):
        user = get_object_or_404(users.models.User, pk=pk)
        if (
            not user.is_active
            and timezone.now() - user.date_joined
            <= timedelta(
                hours=12,
            )
        ):
            user.is_active = True
            user.save()

        return redirect(django.urls.reverse("homepage:home"))


class ReactivateView(django.views.generic.View):
    def get(self, request, pk):
        user = users.models.User.objects.get(pk=pk)
        if user.profile.block_date + timedelta(weeks=1) > timezone.now():
            user.is_active = True
            user.save()

        return redirect(django.urls.reverse("homepage:home"))


class UserListView(django.views.generic.ListView):
    template_name = "users/user_list.html"
    context_object_name = "users"
    queryset = users.models.User.objects.active()


class UserDetailView(django.views.generic.DetailView):
    template_name = "users/user_detail.html"
    context_object_name = "user"
    queryset = users.models.User.objects.active()


class ProfileView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.base.TemplateResponseMixin,
    django.views.generic.View,
):
    template_name = "users/profile.html"

    def get_forms(self, data=None):
        return {
            "user_form": UserChangeForm(data, instance=self.request.user),
            "profile_form": UpdateProfileForm(
                data,
                instance=self.request.user.profile,
            ),
        }

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_forms())

    def post(self, request, *args, **kwargs):
        forms = self.get_forms(request.POST)

        if all(form.is_valid() for form in forms.values()):
            return self.forms_valid(forms)

        return self.forms_invalid(forms)

    def forms_valid(self, forms):
        forms["user_form"].save()
        forms["profile_form"].save()
        messages.success(self.request, "Профиль успешно обновлен")
        return redirect(django.urls.reverse("users:profile"))

    def forms_invalid(self, forms):
        return self.render_to_response(forms)

