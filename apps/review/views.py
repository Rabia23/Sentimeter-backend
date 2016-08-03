from django.contrib.auth.models import User
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.livedashboard import get_live_record
from apps.option.models import Option
from apps.option.utils import option_get, get_related_option
from apps.person.utils import user_get, get_related_user
from apps.review.models import Feedback, FeedbackOption
from apps.review.serializers import FeedbackSerializer
from apps import constants
from apps.utils import save, response, response_json, get_data_param, get_default_param
from apps.redis_queue import RedisQueue
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


class AllFeedback(APIView):

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




