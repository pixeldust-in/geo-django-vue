import logging

from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from .forms import MemberInviteSignupForm
from .models import Invitation

logger = logging.getLogger(__name__)


class InviteSignupView(FormView):
    form_class = MemberInviteSignupForm
    success_url = reverse_lazy("homepage")
    model = Invitation
    template_name = "account/signup.html"

    def get(self, request, *args, **kwargs):
        invitation = self.get_object()
        # To avoid sessions mix up, logout existing users(if any)
        logout(self.request)
        if not invitation:
            messages.error(self.request, "An invalid invitation key was submitted.")
            return redirect(self.success_url)

        if invitation.accepted:
            messages.error(
                self.request,
                f"The invitation for {invitation.email} was already accepted.",
            )

        elif invitation.key_expired():
            messages.error(
                self.request, f"The invitation for {invitation.email} has expired."
            )
            # Redirect to login since there's hopefully an account already.
        else:
            return super().get(request, *args, **kwargs)

        return redirect(self.success_url)

    def get_object(self):
        key = self.kwargs.pop("key", None)
        try:
            return self.model.objects.get(key=key)
        except self.model.DoesNotExist as error:
            logger.warning(f"Key doesn't exist. {error}")
            return None

    def form_valid(self, form):
        invitation = self.get_object()
        if not invitation:
            messages.error(self.request, "An invalid invitation key was submitted.")
            return super().form_valid(form)
        if invitation.accepted:
            messages.error(
                self.request,
                f"The invitation for {invitation.email} was already accepted.",
            )

        elif invitation.key_expired():
            messages.error(
                self.request, f"The invitation for {invitation.email} has expired."
            )
            # Redirect to login since there's hopefully an account already.
        else:
            invitation.accepted = True
            invitation.save()
            user = get_object_or_404(get_user_model(), email=invitation.email)
            user.set_password(form.cleaned_data["password1"])
            user.is_active = True
            user.save()

            messages.success(
                self.request,
                "Account Activated! You can login using your email/mobile & password.",
            )

        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
