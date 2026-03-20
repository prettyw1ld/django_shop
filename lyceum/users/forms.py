__all__ = ()

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
import django.forms

import users.models


class SignUpForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class Profile(django.forms.ModelForm):
    class Meta:
        model = users.models.Profile
        fields = ("image", "bio", "birthday")


class User(django.forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("email", "username", "first_name", "last_name")


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
