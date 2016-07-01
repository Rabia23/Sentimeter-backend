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
from apps.utils import save, response, response_json, get_data_param
from apps.redis_queue import RedisQueue
from apps.livedashboard import get_live_record
from rest_framework.mixins import ListModelMixin
from drf_haystack.generics import HaystackGenericAPIView
from django.db import IntegrityError, transaction
from apps.review.utils import save_feedback


class FeedbackView(APIView):

    def get(self, request, format=None):
        feedback = Feedback.objects.all()
        serializer = FeedbackSerializer(feedback, many=True)
        return Response(response_json(True, serializer.data, None))

    @transaction.atomic
    def post(self, request, format=None):
        status = save_feedback(request.data)
        if status:
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