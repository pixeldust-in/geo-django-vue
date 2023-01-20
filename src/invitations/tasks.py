import logging

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

from celery_app import app
from core.models import User
from core.utils import build_domain_url

logger = logging.getLogger(__name__)


@app.task(bind=True)
def mail_invite_task(self, invite_id, user_uuid, inviter_uuid, *args, **kwargs):  # noqa
    from .models import Invitation  # noqa

    user = User.objects.get(uuid=user_uuid)
    inviter = User.objects.get(uuid=inviter_uuid)
    invite = Invitation.objects.get(id=invite_id)
    logger.info(f"Fetched invite object. Invite ID[{invite.id}]")

    context = {
        "email": invite.email,
        "invite_url": build_domain_url(invite.get_invite_url()),
        "full_name": user.full_name,
        "inviter_full_name": inviter.full_name,
    }
    template_name = "email/invitation.txt"
    html_message = render_to_string(template_name, context)
    send_mail(
        settings.INVITATION_EMAIL_SUBJECT,
        None,
        settings.DEFAULT_FROM_EMAIL,
        [invite.email],
        html_message=html_message,
    )
    logger.info("Invitation Mail sent.")
    invite.sent = timezone.localtime()
    invite.save()
    logger.info("Updated invite record.")
