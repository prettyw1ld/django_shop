__all__ = ()

from django.contrib.auth.forms import UserChangeForm, UserCreationForm
import django.forms

import users.models


class BootrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class UserCreationForm(BootrapFormMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = users.models.User
        fields = (
            users.models.User.username.field.name,
            users.models.User.email.field.name,
        )


class UserChangeForm(BootrapFormMixin, UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = users.models.User
        fields = (
            users.models.User.first_name.field.name,
            users.models.User.last_name.field.name,
        )


class UpdateProfileForm(BootrapFormMixin, django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        coffee_count_field = users.models.Profile.coffee_count.field.name
        self.fields[coffee_count_field].disabled = True

    class Meta:
        model = users.models.Profile
        fields = (
            users.models.Profile.bio.field.name,
            users.models.Profile.birthday.field.name,
            users.models.Profile.image.field.name,
            users.models.Profile.coffee_count.field.name,
        )
        help_texts = {
            users.models.Profile.bio.field.name: "Расскажите о себе",
            users.models.Profile.birthday.field.name: "Укажите дату рождения",
            users.models.Profile.image.field.name: "Загрузите аватарку",
        }
