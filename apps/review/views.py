from django.contrib.auth.models import User
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.option.models import Option
from apps.option.utils import option_get, get_related_option
from apps.person.utils import user_get, get_related_user
from apps.review.models import Feedback, FeedbackOption
from apps.review.serializers import FeedbackSerializer, FeedbackSearchSerializer
from lively import settings
from lively._celery import send_negative_feedback_email
from apps import constants
from apps.utils import save, response, response_json, get_data_param,get_default_param
from apps.redis_queue import RedisQueue
from apps.livedashboard import get_live_record
from rest_framework.mixins import ListModelMixin
from drf_haystack.generics import HaystackGenericAPIView
from django.db import IntegrityError, transaction
from apps.review.utils import save_feedback
from django.core.paginator import Paginator

class FeedbackView(APIView):

    def get(self, request, format=None):
        feedback = Feedback.objects.all()
        serializer = FeedbackSerializer(feedback, many=True)
        return Response(response_json(True, serializer.data, None))

    @transaction.atomic
    def post(self, request, format=None):
        status = save_feedback(request.data)
        if status:
            q = RedisQueue('feedback_redis_queue')
            q.put(str(get_live_record()))
            return Response(response_json(True, None, "Feedback successfully added"))

        return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))


class FeedbackBatchView(APIView):

    @transaction.atomic
    def post(self, request, format=None):
        feedback_array = request.data
        for feedback in feedback_array:
            status = save_feedback(feedback)
            if status == False:
                return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))
        q = RedisQueue('feedback_redis_queue')
        q.put(str(get_live_record()))
        # q.put("ping")
        return Response(response_json(True, None, "Feedback successfully added"))


class AllFeedbackView(APIView):

    def get(self, request, format=None):
        feedback_list = []
        page_data = []

        page_number = get_default_param(request, 'page', 1)
        feedbacks = Feedback.objects.all().order_by("-created_at")

        for feed in feedbacks:
            options_array = []
            options = FeedbackOption.objects.select_related("option").filter(feedback=feed)

            for op in options:
                options_array.append({
                    'option': op.option.text,
                })

            feedback_list.append({"feed":feed.comment,
                                        "options_dict":options_array})

        paginator = Paginator(feedback_list, constants.FEEDBACK_RECORDS_PER_PAGE)

        if paginator.num_pages < int(page_number):
            return Response(response_json(True, page_data, "Page not available"))

        page_data = paginator.page(page_number).object_list

        data = {
            "data": page_data,
            "page_count": paginator.num_pages,
            "record_count": paginator.count,
        }

        return Response(response_json(True, data, None))
# -----------------text local start ----------#

#!/usr/bin/env python

import urllib.request
import urllib.parse

def sendSMS(uname, hashCode, numbers, sender, message):
    data =  urllib.parse.urlencode({'username': uname, 'hash': hashCode, 'numbers': numbers,
        'message' : message, 'sender': sender})
    data = data.encode('utf-8')
    request = urllib.request.Request("http://api.txtlocal.com/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return(fr)
def MessageFeedBackView(request):
    resp =  sendSMS('zamanafzal@gmail.com', 'c7f22503211dde7529015fb648efe42edcd30ede', '923146114223',
        'Mcdonalds', 'This is sample message for mcdonalds feedback.')
    print (resp)


#!/usr/bin/env python

import urllib.request
import urllib.parse

def getInboxes(uname, hashCode):
    data =  urllib.parse.urlencode({'username': uname, 'hash': hashCode})
    data = data.encode('utf-8')
    request = urllib.request.Request("http://api.txtlocal.com/get_inboxes/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return(fr)


def MessageFeedBackViewRec(request):
    resp =  getInboxes('zamanafzal@gmail.com', 'c7f22503211dde7529015fb648efe42edcd30ede')
    print (resp)


# -----------------text local end ----------#



# ----------------- plivo start ----------#
import plivo
def plivo_message_send(request):
    # -*- coding: utf-8 -*-


    auth_id = "MAMWM1MZG2M2EZODE1ZT"
    auth_token = "MmYzNWE5ZTE0OTgzMmU2YzU1ZjdkNzhjOWMxNTE1"

    p = plivo.RestAPI(auth_id, auth_token)

    params = {
        'src': 'ALPHA-ID',  # Alphanumeric sender ID
        'dst': '923146114223',  # Receiver's phone number with ountry code
        'text': "Hi, text from Plivo"  # Your SMS text message
    }

    response = p.send_message(params)

    # Prints the complete response
    print("1 of plivo")
    print(str(response))

    # Sample successful output
    # (202,
    # {
    #               u'message': u'message(s) queued',
    #               u'message_uuid': [u'b795906a-8a79-11e4-9bd8-22000afa12b9'],
    #               u'api_id': u'b77af520-8a79-11e4-b153-22000abcaa64'
    #       }
    # )

    # Prints only the status code
    print("2 of plivo")
    print(str(response[0]))

    # Sample successful output
    # 202

    # Prints the message details
    print("3 of plivo")
    print(str(response[1]))

    # Sample successful output
    # {
    #       u'message': u'message(s) queued',
    #       u'message_uuid': [u'b795906a-8a79-11e4-9bd8-22000afa12b9'],
    #       u'api_id': u'b77af520-8a79-11e4-b153-22000abcaa64'
    # }

    # Print the message_uuid
    print("4 of plivo")
    # print(str(response[1]['message_uuid']))

    # Sample successful output
    # [u'b795906a-8a79-11e4-9bd8-22000afa12b9']

    # Print the api_id
    print("5 of plivo")
    print(str(response[1]['api_id']))

    # Sample successful output
    # b77af520-8a79-11e4-b153-22000abcaa64


# ----------------- plivo end ----------#




# ----------------- twillio start ----------#




from twilio.rest import TwilioRestClient

def twillio_message_send(request):

    # Find these values at https://twilio.com/user/account
    account_sid = "AC6b17872c1aac640d1a0c56182f026f44"
    auth_token = "5c3508333e7bcbecf5babccce4cee95c"
    client = TwilioRestClient(account_sid, auth_token)

    message = client.messages.create(to="+923146114223", from_="+12677336602",
                                         body="Hello zaman!How are you?")
    print("sent")
    print(message)






from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from django_twilio.decorators import twilio_view
from twilio.twiml import Response

TWILIO_ACCOUNT_SID = "AC6b17872c1aac640d1a0c56182f026f44"
TWILIO_AUTH_TOKEN = "5c3508333e7bcbecf5babccce4cee95c"

@twilio_view
def sms(request):
    r = Response()
    print('r is',r)
    r.message('Hello world! Get in touch - paul@twilio.com')
    return r


@twilio_view
def ring(request):
    r = Response()
    r.play('http://bit.ly/phaltsw')
    return r

# This is a plain view that returns manually written TwiML
# Note: it's not linked to a URL in this example.
@csrf_exempt
def sms_plain(request):
    twiml = '<Response><Message>Plain old TwiML</Message></Response>'
    return HttpResponse(twiml, content_type='text/xml')


# This is an example that looks for a parameter in the request
# and returns a personalised message
@twilio_view
def sms_personal(request):
    name = request.POST.get('Body', '')
    msg = 'Hey %s, how are you today?' % (name)

    r = Response()
    r.message(msg)