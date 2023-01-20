from django.urls import path

from .views import InviteSignupView

app_name = "invitations"

urlpatterns = [
    path(
        "invitation/signup/<key>/",
        InviteSignupView.as_view(),
        name="accept_invite_signup",
    )
]
