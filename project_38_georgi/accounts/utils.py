from twilio.rest import Client
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_sms(to_number, message):
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to_number
        )
    except Exception as e:
        logger.error(f"Failed to send SMS: {e}")
        raise
