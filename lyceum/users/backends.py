__all__ = ()

from django.conf import settings
import django.contrib.auth
import django.core.mail
from django.utils import timezone

import users.models


class AuthBackend(django.contrib.auth.backends.ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            if "@" in username:
                user = users.models.User.objects.by_mail(username)
            else:
                user = users.models.User.objects.get(username=username)
        except users.models.User.DoesNotExist:
            return None
        else:
            if not hasattr(user, "profile"):
                users.models.Profile.objects.create(user=user)

            if user.check_password(password):
                user.profile.attempts_count = 0
                user.profile.save()
                return user

            user.profile.attempts_count += 1
            if user.profile.attempts_count >= settings.MAX_AUTH_ATTEMPTS:
                user.is_active = False
                user.profile.block_date = timezone.now()
                user.save()
                activate_url = django.urls.reverse(
                    "users:reactivate",
                    kwargs={"pk": user.id},
                )
                django.core.mail.send_mail(
                    subject="Блокировка аккаунта",
                    message=f"Ваш аккаунт был заблокирован из-за "
                    "слишком большого количества неудачных попыток входа. "
                    "Для разблокировки перейдите по ссылке:"
                    f"\n{activate_url}\n\nСсылка действительна 7 часов.",
                    from_email=settings.DJANGO_MAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )

            user.profile.save()

        return None
