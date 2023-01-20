# Create your models here.
import datetime

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone

from core.utils import mask_str

from .managers import InvitationManager


class Invitation(models.Model):
    email = models.EmailField(
        unique=True,
        verbose_name="e-mail address",
        max_length=settings.EMAIL_MAX_LENGTH,
    )
    created = models.DateTimeField(verbose_name="created", auto_now_add=True)
    accepted = models.BooleanField(verbose_name="accepted", default=False)
    key = models.CharField(verbose_name="key", max_length=64, unique=True)
    sent = models.DateTimeField(verbose_name="sent", null=True, blank=True)

    objects = InvitationManager()

    def __str__(self):
        return "Invite: {0}".format(self.email)

    def key_expired(self):
        expiration_date = self.sent + datetime.timedelta(
            days=settings.INVITATION_EXPIRY_DAYS
        )
        return expiration_date <= timezone.localtime()

    def get_invite_url(self):
        return reverse("invitations:accept_invite_signup", args={self.key})

    @property
    def masked_key(self):
        if self.key:
            return mask_str(self.key, skip_count=10)
        return None
