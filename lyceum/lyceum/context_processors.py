__all__ = ()

import django.utils.timezone

from users.models import User


def birthdays(request):
    time_now = django.utils.timezone.localdate()
    return {
        "birthdays_users": User.objects.filter(
            profile__birthday__month=time_now.month,
            profile__birthday__day=time_now.day,
            is_active=True,
        ).values("first_name", "email"),
    }
