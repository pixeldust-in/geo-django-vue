# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from . import managers
from .mixins import AbstractTrack


class User(AbstractUser, AbstractTrack):
    full_name = models.CharField(max_length=50)
    email = models.EmailField(
        _("email address"),
        unique=True,
    )
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    manager = managers.UserManager()

    def save(self, *args, **kwargs):
        self.username = self.email
        super().save(*args, **kwargs)
