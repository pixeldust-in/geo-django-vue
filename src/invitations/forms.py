from django.contrib.auth.forms import UserCreationForm

from core import models as core_models


class MemberInviteSignupForm(UserCreationForm):
    class Meta:
        fields = ("password1", "password2")
        model = core_models.User
