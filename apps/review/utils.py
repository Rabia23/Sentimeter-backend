from apps import constants
from apps.review.enum import ActionStatusEnum
from apps.utils import make_request, response_json
from lively._celery import send_negative_feedback_email
from apps.review.serializers import FeedbackSerializer
from apps.person.utils import get_related_user
from apps.review.models import FeedbackOption
from lively import settings
from rest_framework.response import Response
from pytz import timezone
from datetime import datetime


__author__ = 'aamish'


def feedback_get(object_id):
    response = make_request('GET', "application/json", '/1/classes/Feedback/%s' % object_id, '')
    return response


def get_converted_time(date):
    return datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f+00").replace(tzinfo=timezone('UTC'))


def save_feedback(data):
    if "user" in data:
        user_data = data["user"]
        user = get_related_user(user_data)
    else:
        user = None

    feedback_params = data
    feedback_params['user'] = user.id if user else None

    serializer = FeedbackSerializer(data=data)
    if serializer.is_valid():
        feedback = serializer.save()
        if feedback:
            if "options" in data:
                options_list = data["options"]

                for option_id in options_list:
                    if "created_at" in data:
                        feedback_option = FeedbackOption(feedback=feedback, option_id=option_id)
                        feedback_option.save()
                        date = get_converted_time(data["created_at"])
                        feedback_option.save_date(date)
                    else:
                        FeedbackOption(feedback=feedback, option_id=option_id).save()

            if "created_at" in data:
                date = get_converted_time(data["created_at"])
                feedback.save_date(date)

            feedback.mark_feedback_status()
            feedback.keyword_analysis()
            feedback.mark_segment()

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

            return True
    return False


def generate_missing_actions(data):
    list_actions = [item['action_taken'] for item in data]
    list_feedback = list(data)

    if ActionStatusEnum.UNPORCESSED not in list_actions:
        list_feedback.append(
            {'count': 0, 'action_taken': ActionStatusEnum.UNPORCESSED}
        )
    if ActionStatusEnum.RECOVERED not in list_actions:
        list_feedback.append(
            {'count': 0, 'action_taken': ActionStatusEnum.RECOVERED}
        )
    if ActionStatusEnum.UNRECOVERABLE not in list_actions:
        list_feedback.append(
            {'count': 0, 'action_taken': ActionStatusEnum.UNRECOVERABLE}
        )

    if ActionStatusEnum.NOACTIONNEEDED not in list_actions:
        list_feedback.append(
            {'count': 0, 'action_taken': ActionStatusEnum.NOACTIONNEEDED}
        )

    return list_feedback


# def generate_actions_with_action_texts(data):
#     response_list = []
#     action = "Invalid"
#     for item in data:
#         if item["action_taken"] == constants.PROCESSED:
#             action = "Processed"
#         elif item["action_taken"] == constants.UNPROCESSED:
#             action = "Unprocessed"
#         elif item["action_taken"] == constants.DEFERRED:
#             action = "Deferred"
#         response_list.append({'count': item["count"], 'action_taken': action})
#     return response_list


def valid_action_id(action_id):
    return True if action_id == 1 or action_id == 2 or action_id ==3 else False
