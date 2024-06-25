# test_twilio.py
from twilio.rest import Client

account_sid = 'your_twilio_account_sid'
auth_token = 'your_twilio_auth_token'
client = Client(account_sid, auth_token)

message = client.messages.create(
    body="Hello from Python",
    from_='your_twilio_phone_number',
    to='recipient_phone_number'
)

print(message.sid)