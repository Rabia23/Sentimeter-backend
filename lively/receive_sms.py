__author__ = 'rabia'
# from twilio.rest import TwilioRestClient
#
# # To find these visit https://www.twilio.com/user/account
# ACCOUNT_SID = "AC58772f5421152c63fed847d2285bc1ed"
# AUTH_TOKEN = "c94609ae27a609f0e19c43187a55d692"
#
# client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
#
# message = client.messages.create(
#     body="Hello From Twilio!",  # Message body, if any
#     to="+923244568127",
#     from_="+12013800760",
# )
# print(message.sid)


from django_twilio.decorators import twilio_view
from twilio.twiml import Response

@twilio_view
def sms(request):
    print("receiving sms")
    r = Response()
    print(r)
    r.message('Hello from your Django app!')
    return r
