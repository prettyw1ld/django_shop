import django.contrib.auth.views
import django.urls

import users.views

app_name = "users"

login_view = users.views.LoginView.as_view(
    template_name="users/login.html",
)

logout_view = django.contrib.auth.views.LogoutView.as_view(
    template_name="users/logout.html",
)

password_change_view = django.contrib.auth.views.PasswordChangeView.as_view(
    template_name="users/password_change.html",
)

password_change_done_view = (
    django.contrib.auth.views.PasswordChangeDoneView.as_view(
        template_name="users/password_change_done.html",
    )
)

password_reset_view = django.contrib.auth.views.PasswordResetView.as_view(
    template_name="users/password_reset.html",
)

password_reset_done_view = (
    django.contrib.auth.views.PasswordResetDoneView.as_view(
        template_name="users/password_reset_done.html",
    )
)

password_reset_confirm_view = (
    django.contrib.auth.views.PasswordResetConfirmView.as_view(
        template_name="users/password_reset_confirm.html",
    )
)

password_reset_complete_view = (
    django.contrib.auth.views.PasswordResetCompleteView.as_view(
        template_name="users/password_reset_complete.html",
    )
)

signup_view = users.views.SignUpView.as_view()
activate_view = users.views.ActivateView.as_view()
reactivate_view = users.views.ReactivateView.as_view()
user_detail_view = users.views.UserDetailView.as_view()
user_list_view = users.views.UserListView.as_view()
profile_view = users.views.ProfileView.as_view()

urlpatterns = [
    django.urls.path("login/", login_view, name="login"),
    django.urls.path("logout/", logout_view, name="logout"),
    django.urls.path(
        "password_change/",
        password_change_view,
        name="password_change",
    ),
    django.urls.path(
        "password_change_done/",
        password_change_done_view,
        name="password_change_done",
    ),
    django.urls.path(
        "password_reset/",
        password_reset_view,
        name="password_reset",
    ),
    django.urls.path(
        "password_reset_done/",
        password_reset_done_view,
        name="password_reset_done",
    ),
    django.urls.path(
        "password_reset_confirm/<uidb64>/<token>/",
        password_reset_confirm_view,
        name="password_reset_confirm",
    ),
    django.urls.path(
        "password_reset_complete/",
        password_reset_complete_view,
        name="password_reset_complete",
    ),
    django.urls.path(
        "signup/",
        signup_view,
        name="signup",
    ),
    django.urls.path(
        "activate/<pk>/",
        activate_view,
        name="activate",
    ),
    django.urls.path(
        "reactivate/<pk>/",
        reactivate_view,
        name="reactivate",
    ),
    django.urls.path(
        "<int:pk>/",
        user_detail_view,
        name="user-detail",
    ),
    django.urls.path("", user_list_view, name="user-list"),
    django.urls.path(
        "profile/",
        profile_view,
        name="profile",
    ),
]
