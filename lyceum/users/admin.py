__all__ = ()

import django.contrib.admin
import django.contrib.auth.models

import users.models


class ProfileInline(django.contrib.admin.StackedInline):
    model = users.models.Profile
    list_display = (users.models.Profile.coffee_count.field.name,)
    fields = (
        users.models.Profile.bio.field.name,
        users.models.Profile.birthday.field.name,
        users.models.Profile.image.field.name,
        users.models.Profile.coffee_count.field.name,
    )
    readonly_fields = (users.models.Profile.coffee_count.field.name,)


django.contrib.admin.site.unregister(django.contrib.auth.models.User)


@django.contrib.admin.register(django.contrib.auth.models.User)
class UserAdmin(django.contrib.admin.ModelAdmin):
    inlines = (ProfileInline,)
    list_display = ("username", "email", "get_coffee_count")

    def get_coffee_count(self, obj):
        return obj.profile.coffee_count

    get_coffee_count.short_description = "Кофе"
