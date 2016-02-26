from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.livedashboard import get_live_record
from apps.option.utils import option_get, get_related_option
from apps.person.utils import user_get, get_related_user
from apps.review.models import Feedback, FeedbackOption
from apps.review.serializers import FeedbackSerializer
from lively import settings
from lively._celery import send_negative_feedback_email
from apps import constants
from apps.utils import save, response, response_json
from apps.redis_queue import RedisQueue


class FeedbackView(APIView):

    def get(self, request, format=None):
        feedback = Feedback.objects.all()
        serializer = FeedbackSerializer(feedback, many=True)
        return Response(response_json(True, serializer.data, None))

    @transaction.atomic
    def post(self, request, format=None):
        data = request.data["object"]
        trigger = request.data["triggerName"]

        if trigger == constants.TRIGGER_AFTER_SAVE:
            if "user" in data:
                related_user = user_get(data["user"]["objectId"])
                user = get_related_user(related_user)
            else:
                user = None

            if "gro_id" in data:
                gro = User.objects.get(pk=data["gro_id"])
            else:
                gro = None

            feedback_params = data
            feedback_params['gro'] = gro.id if gro else None
            feedback_params['user'] = user.id if user else None
            feedback_params['branch'] = data["branch_id"]

            feedback = Feedback.get_if_exists(data["objectId"])
            serializer = FeedbackSerializer(feedback, data=feedback_params)
            feedback = save(serializer)

            if "options" in data:
                for option_data in data["options"]:
                    option_parse = option_get(option_data["objectId"])
                    option = get_related_option(option_parse)

                    feedback_option = FeedbackOption.get_if_exists(feedback.id, option.id)
                    if not feedback_option:
                        FeedbackOption(feedback=feedback, option=option).save()

            feedback.mark_feedback_status()
            feedback.keyword_analysis()

            q = RedisQueue('feedback_redis_queue')
            q.put(str(get_live_record()))
            # q.put("ping")

            if feedback.is_negative() and feedback.not_empty():
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

            return response(data)




