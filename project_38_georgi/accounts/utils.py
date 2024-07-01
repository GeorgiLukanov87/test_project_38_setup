import logging

from twilio.rest import Client
from django.core.mail import send_mail
from django.conf import settings

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


def send_test_email():
    subject = 'Test Email from Django'
    message = 'This is a test email sent from Django.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['badgosho@abv.bg']

    send_mail(subject, message, email_from, recipient_list)
