from django.core.mail import send_mail
from celery import shared_task
import logging
from mad_notifications.models import Notification

logger = logging.getLogger(__name__)

@shared_task(name="Non-Periodic: Email notification")
def email_notification(notification_id):
    try:
        notification_obj = Notification.objects.get(id=notification_id)

        # send email
        send_mail(
            subject = notification_obj.title,
            message = notification_obj.content,
            recipient_list = [notification_obj.user.email],
            fail_silently = False,
        )

    except Exception as e:
        logger.warn(str(e))
