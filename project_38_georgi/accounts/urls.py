from django.urls import path

from project_38_georgi.accounts.views import index, send_email_view, send_sms_view

urlpatterns = [
    path('', index, name='index'),
    path('send-email/', send_email_view, name='send_email'),
    path('send-sms/', send_sms_view, name='send_sms'),

]
# urls.py

