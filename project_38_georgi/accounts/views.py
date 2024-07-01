from django.http import HttpResponse
from django.shortcuts import render
from .utils import send_sms, send_test_email


def index(request):
    return render(request, 'test.html')


def send_email_view(request):
    if request.method == 'POST':
        send_test_email()
        return render(request, 'email_sent.html')
    return render(request, 'send_email.html')


def send_sms_view(request):
    if request.method == 'POST':
        to_number = request.POST.get('to_number')
        message = request.POST.get('message')
        if not to_number or not message:
            return HttpResponse("Phone number and message are required.", status=400)
        try:
            send_sms(to_number, message)
            return render(request, 'sms_sent.html')
        except Exception as e:
            return HttpResponse(f"Failed to send SMS: {e}", status=500)
    return render(request, 'send_sms.html')
