import logging

from django.db import models
from django.utils.crypto import get_random_string

from core.models import User

from . import tasks

logger = logging.getLogger(__name__)


class InvitationManager(models.Manager):
    def create_invitation(self, user_uuid, inviter_uuid):
        """
        Creates an invitation and mails it to the provided email ID.
        """
        try:
            user_email = User.objects.get(uuid=user_uuid).email
            invite = self._create_invite(email=user_email)
            tasks.mail_invite_task.delay(
                user_uuid=user_uuid,
                inviter_uuid=inviter_uuid,
                invite_id=invite.id,
            )
            invite.save()
            return {
                "success": True,
            }
        except Exception as error:
            logger.exception("An exception occurred: {error}")
            return {"success": False, "error": str(error)}

    def _create_invite(self, email):
        """
        Creates and returns an invitation entry. If already exists refreshes the key, accepted and sent values.
        """
        key = get_random_string(64).lower()
        instance, created = self.get_or_create(email=email)
        instance.key = key
        if not created:
            instance.accepted = False
            instance.sent = None
        instance.save()
        return instance
