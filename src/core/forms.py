from allauth.account.forms import LoginForm


class CustomLoginForm(LoginForm):
    def login(self, *args, **kwargs):
        return super().login(*args, **kwargs)
