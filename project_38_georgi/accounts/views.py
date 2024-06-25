from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render


def index(request):
    return render(request, 'test.html')


def send_test_email():
    subject = 'Test Email from Django'
    message = 'This is a test email sent from Django.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['badgosho@abv.bg']

    send_mail(subject, message, email_from, recipient_list)


def send_email_view(request):
    if request.method == 'POST':
        send_test_email()
        return render(request, 'email_sent.html')
    return render(request, 'send_email.html')
