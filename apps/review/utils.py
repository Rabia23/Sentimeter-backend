from apps import constants
from apps.review.enum import ActionStatusEnum
from apps.utils import make_request

__author__ = 'aamish'


def feedback_get(object_id):
    response = make_request('GET', "application/json", '/1/classes/Feedback/%s' % object_id, '')
    return response


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