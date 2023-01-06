from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampTrack(models.Model):
    created = models.DateTimeField(_("created at"), auto_now_add=True)
    modified = models.DateTimeField(_("modified at"), auto_now=True)

    class Meta:
        abstract = True


class UuidMixin(models.Model):
    uuid = models.UUIDField(
        _("uuid field"),
        unique=True,
        default=uuid4,
        editable=False,
    )

    class Meta:
        abstract = True


class AbstractTrack(TimeStampTrack, UuidMixin):
    class Meta:
        abstract = True
