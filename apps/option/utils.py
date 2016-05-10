from apps.option.models import Option
from apps.option.serializers import OptionSerializer
from apps import constants
from apps.review.enum import SegmentEnum
from apps.utils import make_request
from operator import itemgetter


__author__ = 'aamish'


def option_get(object_id):
    response = make_request('GET', "application/json", '/1/classes/Option/%s' % object_id, '')
    return response


def get_related_option(data):
    option = Option.get_if_exists(data["objectId"])
    if option:
        serializer = OptionSerializer(option, data=data)
    else:
        serializer = OptionSerializer(data=data)

    if serializer.is_valid():
        option = serializer.save()

        if "subOptions" in data:
            for sub_option_data in data["subOptions"]:
                sub_option_parse = option_get(sub_option_data["objectId"])
                sub_option = get_related_option(sub_option_parse)

                sub_option.parent = option
                sub_option.save()

        return option


def generate_missing_options(question, data, is_parent_needed=True):
    list_feedback_option_ids = []
    list_feedback = []

    if data:
        list_feedback_option_ids = [item['option_id'] for item in data]
        list_feedback = list(data)

    for option in question.options.all():
        if option.id not in list_feedback_option_ids:
            if is_parent_needed:
                list_feedback.append({'count': 0,
                                      'option_id': option.id,
                                      'option__text': option.text,
                                      'option__parent_id': option.parent_id,
                                      'option__score': option.score,
                                      'option__color_code': option.color_code})
            else:
                list_feedback.append({'count': 0,
                                      'option_id': option.id,
                                      'option__text': option.text,
                                      'option__score': option.score,
                                      'option__color_code': option.color_code})

    return list_feedback


def generate_missing_sub_options(option, data, is_parent_needed=True):
    list_feedback_option_ids = [item['option_id'] for item in data]
    list_feedback = list(data)

    for option in Option.objects.filter(parent=option):
        if option.id not in list_feedback_option_ids:
            if is_parent_needed:
                list_feedback.append({'count': 0,
                                      'option_id': option.id,
                                      'option__text': option.text,
                                      'option__parent_id': option.parent_id,
                                      'option__color_code': option.color_code})
            else:
                list_feedback.append({'count': 0,
                                      'option_id': option.id,
                                      'option__text': option.text,
                                      'option__color_code': option.color_code})

    return list_feedback


def generate_segmentation(data):
    segments_list = []
    for segment in constants.segments:
        segment_feedbacks = [feedback_option for feedback_option in data if feedback_option.feedback.get_segment() == constants.segments[segment]]

        segments_list.append({
            "segment_end_time": segment,
            "segment": constants.segments[segment],
            "option_count": len(segment_feedbacks),
        })
    return sorted(segments_list, key=itemgetter('segment_end_time'))


def generate_segmentation_with_options(data, options, feedback=None):
    segments_list = []
    for label, item in SegmentEnum.items():
        segment_feedback_options = data.filter(feedback__segment=item)
        segment_feedback_count = feedback.filter(segment=item).count() if feedback else None

        segments_list.append({
            "segment_key": item,
            "segment": SegmentEnum.label(item),
            "feedback_count": segment_feedback_count,
            "option_count": segment_feedback_options.count(),
            "option_data": generate_option_group(segment_feedback_options, options)
        })
    return sorted(segments_list, key=itemgetter('segment_key'))


def generate_option_groups(data, options):
    option_groups = []
    for option in options:
        segment_list = generate_segmentation(data.filter(option=option))
        option_groups.append({
            "option__text": option.text,
            "option_id": option.id,
            "segment_list": segment_list,
            "option__color_code": option.color_code,
        })
    return option_groups


def generate_option_group(data, options):
    option_groups = []
    for option in options:
        option_count = data.filter(option_id=option.id).count()
        option_groups.append({
            "option__text": option.text,
            "option_id": option.id,
            "count": option_count,
            "option__color_code": option.color_code,
        })
    return option_groups
