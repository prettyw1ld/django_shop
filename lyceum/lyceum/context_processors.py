__all__ = ()

from users.models import User


def birthdays(request):
    return {
        "birthdays_users": User.objects.filter(
            profile__birthday__isnull=False,
            is_active=True,
        ).values("first_name", "email", "profile__birthday"),
    }
