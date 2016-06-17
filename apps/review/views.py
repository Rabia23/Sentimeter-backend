from django.contrib.auth.models import User
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.livedashboard import get_live_record
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
from rest_framework.mixins import ListModelMixin
from drf_haystack.generics import HaystackGenericAPIView
from django.db import IntegrityError, transaction


class FeedbackView(APIView):

    def get(self, request, format=None):
        feedback = Feedback.objects.all()
        serializer = FeedbackSerializer(feedback, many=True)
        return Response(response_json(True, serializer.data, None))

    @transaction.atomic
    def post(self, request, format=None):
        if "user" in request.data:
            user_data = request.data["user"]
            user = get_related_user(user_data)
        else:
            user = None

        feedback_params = request.data
        feedback_params['user'] = user.id if user else None

        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            feedback = serializer.save()
            if feedback:
                if "options" in request.data:
                    options_list = request.data["options"]

                    for option_id in options_list:
                        FeedbackOption(feedback=feedback, option_id=option_id).save()

                feedback.mark_feedback_status()
                feedback.keyword_analysis()
                feedback.mark_segment()

                # q = RedisQueue('feedback_redis_queue')
                # q.put(str(get_live_record()))
                # q.put("ping")

                if feedback.is_negative() and feedback.not_empty():
                    feedback.mark_for_report()
                    feedback_json = {
                        "is_bad": feedback.is_bad(),
                        "branch_name": feedback.branch.name,
                        "branch_id": feedback.branch.id,
                        "city_name": feedback.branch.city.name,
                        "customer_name": feedback.customer_name(),
                        "customer_phone": feedback.customer_phone(),
                        "customer_email": feedback.customer_email(),
                        "problems": feedback.problems(),
                        "comment": feedback.comment,
                        "server_link": settings.server_url,
                    }

                    # send_negative_feedback_email(feedback_json)
                    send_negative_feedback_email.delay(feedback_json)

                return Response(response_json(True, None, None))
        return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))




