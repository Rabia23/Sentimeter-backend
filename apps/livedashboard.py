from apps.utils import get_next_day

__author__ = 'aamish'

from django.db.models import Count
from apps.area.models import Area
from apps.option.utils import generate_missing_options, generate_segmentation_with_options, generate_segmentation
from apps.question.models import Question
from apps.review.models import FeedbackOption, Feedback, Concern
from apps.review.utils import generate_missing_actions
from apps.serializers import ObjectSerializer
from apps import constants
from dateutil import rrule
from datetime import datetime, timedelta
from django.utils import timezone
from operator import itemgetter
import json


def get_complaint_view(date_from, date_to):
    complaint_view_list = []

    feedback = Feedback.manager.date(date_from, date_to)
    filtered_feedback = feedback.values('action_taken').annotate(count=Count('action_taken'))
    filtered_feedback = generate_missing_actions(filtered_feedback)

    data = {'feedback_count': feedback.count(), 'action_analysis': filtered_feedback}
    complaint_view_list.append({'object': {"id": "", "name": "Pakistan", "objectId": ""}, 'data': data})

    for object in Area.objects.all():
        feedback = Feedback.manager.date(date_from, date_to).related_filters(0, object)
        filtered_feedback = feedback.values('action_taken').annotate(count=Count('action_taken'))
        filtered_feedback = generate_missing_actions(filtered_feedback)

        data = {'feedback_count': feedback.count(), 'action_analysis': filtered_feedback}
        complaint_view_list.append({'object': ObjectSerializer(object).data, 'data': data})

    return complaint_view_list


def get_top_concers():
    concerns = [concern.to_dict() for concern in Concern.objects.filter(is_active=True).order_by("-count")[:5]]
    return {'concern_count': len(concerns), 'concern_list': concerns}


def get_top_segment(date_from, date_to):
    question = Question.objects.get(type=constants.TYPE_1)

    options = question.options.all()
    feedback_options = FeedbackOption.manager.options(options).date(date_from, date_to)

    feedback_segmented_list = generate_segmentation(feedback_options)
    feedback_segmented_counts = [segment["option_count"] for segment in feedback_segmented_list]
    return feedback_segmented_list[feedback_segmented_counts.index(max(feedback_segmented_counts))]


def get_overall_feedback(date_from, date_to):
    feedback_options = FeedbackOption.manager.question(constants.TYPE_1).date(date_from, date_to)
    feedback_options_dict = feedback_options.values('option_id', 'option__text', 'option__score').\
        annotate(count=Count('option_id'))
    list_feedback = generate_missing_options(Question.objects.get(type=constants.TYPE_1), feedback_options_dict, False)

    return {'feedback_count': feedback_options.count(), 'feedbacks': sorted(list_feedback, reverse=True, key=itemgetter('option__score'))}


def get_segmentation_rating(date_from, date_to):
    question = Question.objects.get(type=constants.TYPE_2)

    options = question.options.all()

    feedback_options = FeedbackOption.manager.options(question.options.all()).date(date_from, date_to)
    feedback_segmented_list = generate_segmentation_with_options(feedback_options, options)

    return {'segment_count': len(feedback_segmented_list), 'segments': feedback_segmented_list}


def get_top_rankings(date_from=None, date_to=None):
    overall_experience = FeedbackOption.get_top_option(date_from, date_to)
    positive_negative_feedback = Feedback.get_feedback_type_count(date_from, date_to)
    qsc_count = FeedbackOption.get_qsc_count(date_from, date_to)

    return {'overall_experience': overall_experience,
            'top_segment': get_top_segment(date_from, date_to),
            'positive_negative_feedback': positive_negative_feedback,
            'qsc_count': qsc_count}


def get_leaderboard_view(date_from, date_to):
    city = Feedback.get_top_city(date_from, date_to)
    branches = Feedback.get_top_branches(date_from, date_to)
    gro = Feedback.get_top_gro(date_from, date_to)

    return {'city': city, "branches": branches, "gro": gro}


def get_overall_rating(date_from, date_to):
    feedback_records_list = []

    current_tz = timezone.get_current_timezone()
    date_from = current_tz.localize(datetime.strptime(date_from + " 00:00:00", constants.DATE_FORMAT))
    date_to = current_tz.localize(datetime.strptime(date_to + " 23:59:59", constants.DATE_FORMAT))

    rule = rrule.DAILY
    question = Question.objects.get(type=constants.TYPE_2)
    for single_date in rrule.rrule(rule, dtstart=date_from, until=date_to):
        feedback_options = FeedbackOption.manager.date(str(single_date.date()), str(single_date.date()))
        feedback_options = feedback_options.question_parent_options(question)
        filtered_feedback = feedback_options.values('option_id', 'option__text', 'option__score').annotate(count=Count('option_id'))
        list_feedback = generate_missing_options(question, filtered_feedback, False)

        date_data = {'feedback_count': feedback_options.count(), 'feedbacks': list_feedback}
        feedback_records_list.append({'date': single_date.strftime('%Y-%m-%d'), 'data': date_data})

    if len(feedback_records_list) > constants.NO_OF_DAYS:
        feedback_records_list = feedback_records_list[-constants.NO_OF_DAYS:]

    return feedback_records_list


def get_opportunity_analysis(date_from, date_to):
    feedback_options = FeedbackOption.manager.question(constants.TYPE_3).date(date_from, date_to)
    feedback_options_dict = feedback_options.values('option_id', 'option__text', 'option__parent_id', 'option__score').\
            annotate(count=Count('option_id'))

    list_feedback = generate_missing_options(Question.objects.get(type=constants.TYPE_3), feedback_options_dict)
    return {'feedback_count': feedback_options.count(), 'feedbacks': list_feedback}


def get_live_record():
    now = datetime.now()

    date_to_str = str(now.date())
    date_from_str = str((now - timedelta(days=1)).date())

    data = {
        "segmentation_rating": get_segmentation_rating(date_from_str, date_to_str),
        "overall_feedback": get_overall_feedback(date_from_str, date_to_str),
        "overall_rating": get_overall_rating(str((now - timedelta(days=constants.NO_OF_DAYS)).date()), date_to_str),
        "complaint_view": get_complaint_view(date_from_str, date_to_str),
        "top_rankings": get_top_rankings(date_from_str, date_to_str),
        "leaderboard_view": get_leaderboard_view(date_from_str, date_to_str),
        "concerns": get_top_concers(),
        "strength": get_opportunity_analysis(date_from_str, date_to_str),
    }

    return json.dumps(data)