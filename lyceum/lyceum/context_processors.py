__all__ = ()


def birthdays(request):
    from users.models import User
    import django.utils.timezone

    time_now = django.utils.timezone.now()
    return {
        "birthdays_users": User.objects.filter(
            profile__birthday__month=time_now.month,
            profile__birthday__day=time_now.day,
            is_active=True,
        ).values("first_name", "email", "profile__birthday"),
    }
