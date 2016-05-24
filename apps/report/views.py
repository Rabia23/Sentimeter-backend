from django.db.models import Count
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.area.models import Area
from apps.option.utils import generate_missing_options, generate_segmentation_with_options, generate_segmentation
from apps.person.enum import UserAgeEnum
from apps.person.utils import generate_gender_division
from apps.question.models import Question
from apps.review.models import FeedbackOption, Feedback, Concern
from apps.review.utils import generate_missing_actions
from apps.serializers import ObjectSerializer
from dateutil import rrule
from django.utils import timezone
from operator import itemgetter
from apps.decorators import my_login_required
from apps.utils import response_json, get_user_data, get_param
from django.utils.decorators import method_decorator
from datetime import datetime, timedelta
from apps import constants

# Create your views here.
class ReportView(APIView):

    def _get_complaint_view(self, date_from, date_to, region_id, city_id, branch_id):
        complaint_view_list = []

        feedback = Feedback.manager.date(date_from, date_to).filters(region_id, city_id, branch_id)
        filtered_feedback = feedback.values('action_taken').annotate(count=Count('action_taken'))
        filtered_feedback = generate_missing_actions(filtered_feedback)

        data = {'feedback_count': feedback.count(), 'action_analysis': filtered_feedback}
        complaint_view_list.append({'object': {"id": "", "name": "Pakistan", "objectId": ""}, 'data': data})

        for object in Area.objects.all():
            feedback = Feedback.manager.date(date_from, date_to).related_filters(0, object).filters(region_id, city_id, branch_id)
            filtered_feedback = feedback.values('action_taken').annotate(count=Count('action_taken'))
            filtered_feedback = generate_missing_actions(filtered_feedback)

            for feedback_dict in filtered_feedback:
                feedback_dict.update({'color_code': constants.COLORS_ACTION_STATUS[feedback_dict["action_taken"]]})

            data = {'feedback_count': feedback.count(), 'action_analysis': filtered_feedback}
            complaint_view_list.append({'object': ObjectSerializer(object).data, 'data': data})

        return complaint_view_list

    def _get_top_concers(self):
        concerns = [concern.to_dict() for concern in Concern.objects.filter(is_active=True).order_by("-count")[:5]]
        return {'concern_count': len(concerns), 'concern_list': concerns}

    def _get_top_segment(self, date_from, date_to, region_id, city_id, branch_id):
        question = Question.objects.get(type=constants.TYPE_1)

        options = question.options.all()
        feedback_options = FeedbackOption.manager.options(options).date(date_from, date_to)

        feedback_segmented_list = generate_segmentation(feedback_options)
        feedback_segmented_counts = [segment["option_count"] for segment in feedback_segmented_list]
        return feedback_segmented_list[feedback_segmented_counts.index(max(feedback_segmented_counts))]

    def _get_overall_feedback(self, date_from, date_to, region_id, city_id, branch_id):
        feedback_options = FeedbackOption.manager.question(constants.TYPE_1).date(date_from, date_to).filters(region_id, city_id, branch_id)
        feedback_options_dict = feedback_options.values('option_id', 'option__text', 'option__parent_id', 'option__score', 'option__color_code').\
            annotate(count=Count('option_id'))
        list_feedback = generate_missing_options(Question.objects.get(type=constants.TYPE_1), feedback_options_dict)

        return {'feedback_count': feedback_options.count(), 'feedbacks': sorted(list_feedback, reverse=True, key=itemgetter('option__score'))}

    def _get_segmentation_rating(self, date_from, date_to, region_id, city_id, branch_id):

        question = Question.objects.get(type=constants.TYPE_2)
        options = question.options.all()
        feedback_options = FeedbackOption.manager.options(question.options.all()).date(date_from, date_to).filters(region_id, city_id, branch_id)
        feedback_segmented_list = generate_segmentation_with_options(feedback_options, options)

        sub_options_segments_list = []
        for option in options:
            children_options = option.children.all()
            children_feedback_options = FeedbackOption.manager.options(children_options).date(date_from, date_to).filters(region_id, city_id, branch_id)
            children_feedback_segmented_list = generate_segmentation_with_options(children_feedback_options, children_options)
            sub_options_segments_list.append({'sub_option_segments_list': children_feedback_segmented_list})
        return {'segment_count': len(feedback_segmented_list), 'segments': feedback_segmented_list, 'sub_options_segments': sub_options_segments_list}

    def _get_top_rankings(self, region_id, city_id, branch_id, date_from=None, date_to=None,):
        overall_experience = FeedbackOption.get_top_option(date_from, date_to)
        positive_negative_feedback = Feedback.get_feedback_type_count(date_from, date_to)
        qsc_count = FeedbackOption.get_qsc_count(date_from, date_to)

        return {'overall_experience': overall_experience,
                'top_segment': self._get_top_segment(date_from, date_to, region_id, city_id, branch_id),
                'positive_negative_feedback': positive_negative_feedback,
                'qsc_count': qsc_count}

    def _get_overall_rating(self, date_from, date_to, region_id, city_id, branch_id):
        feedback_records_list = []

        current_tz = timezone.get_current_timezone()
        date_from = current_tz.localize(datetime.strptime(date_from + " 00:00:00", constants.DATE_FORMAT))
        date_to = current_tz.localize(datetime.strptime(date_to + " 23:59:59", constants.DATE_FORMAT))

        rule = rrule.DAILY
        question = Question.objects.get(type=constants.TYPE_2)
        for single_date in rrule.rrule(rule, dtstart=date_from, until=date_to):
            feedback_options = FeedbackOption.manager.date(str(single_date.date()), str(single_date.date())).filters(region_id, city_id, branch_id)
            feedback_options = feedback_options.question_parent_options(question)
            filtered_feedback = feedback_options.values('option_id', 'option__text', 'option__parent_id', 'option__color_code').\
                                    annotate(count=Count('option_id'))
            list_feedback = generate_missing_options(question, filtered_feedback)

            date_data = {'feedback_count': feedback_options.count(), 'feedbacks': list_feedback}
            feedback_records_list.append({'date': single_date.date(), 'data': date_data})

        if len(feedback_records_list) > constants.NO_OF_DAYS:
            feedback_records_list = feedback_records_list[-constants.NO_OF_DAYS:]

        return feedback_records_list

    def _get_opportunity_analysis(self, date_from, date_to, region_id, city_id, branch_id):
        feedback_options = FeedbackOption.manager.question(constants.TYPE_3).date(date_from, date_to).filters(region_id, city_id, branch_id)
        feedback_options_dict = feedback_options.values('option_id', 'option__text', 'option__parent_id', 'option__score', 'option__color_code').\
                annotate(count=Count('option_id'))

        list_feedback = generate_missing_options(Question.objects.get(type=constants.TYPE_3), feedback_options_dict)
        return {'feedback_count': feedback_options.count(), 'feedbacks': list_feedback}

    def _get_customer_analysis(self, date_from, date_to, region_id, city_id, branch_id):
        feedback = Feedback.manager.date(date_from, date_to).filters(region_id, city_id, branch_id)

        customer_analysis = []
        for age in UserAgeEnum.items():
            age_group_feedback = feedback.filter(user__info__ageGroup=age[1])
            customer_analysis.append({
                "age_group_id": age[1],
                "age_group_label": UserAgeEnum.label(age[0]),
                "count": age_group_feedback.count(),
                "gender_division": generate_gender_division(age_group_feedback)
            })

        return {'feedback_count': feedback.count(), 'customer_analysis': customer_analysis}

    def _get_recommendation_analysis(self, date_from, date_to, region_id, city_id, branch_id):
        feedback_options = FeedbackOption.manager.question(constants.TYPE_20).date(date_from, date_to).\
                filters(region_id, city_id, branch_id)
        feedback_options_dict = feedback_options.values('option_id', 'option__text', 'option__parent_id', 'option__score', 'option__color_code').\
            annotate(count=Count('option_id'))

        list_feedback = generate_missing_options(Question.objects.get(type=constants.TYPE_20), feedback_options_dict)

        return {'feedback_count': feedback_options.count(), 'feedbacks': list_feedback}

    @method_decorator(my_login_required)
    def get(self, request, user, format=None):
        try:
            now = datetime.now()
            region_id, city_id, branch_id = get_user_data(user)

            date_to_str = get_param(request, 'date_to', str(now.date()))
            date_from_str = get_param(request, 'date_from', str((now - timedelta(days=1)).date()))

            data = {
                "segmentation_rating": self._get_segmentation_rating(date_from_str, date_to_str, region_id, city_id, branch_id),
                "overall_feedback": self._get_overall_feedback(date_from_str, date_to_str, region_id, city_id, branch_id),
                "overall_rating": self._get_overall_rating(str((now - timedelta(days=constants.NO_OF_DAYS)).date()), date_to_str, region_id, city_id, branch_id),
                "complaint_view": self._get_complaint_view(date_from_str, date_to_str, region_id, city_id, branch_id),
                "top_rankings": self._get_top_rankings(date_from_str, date_to_str, region_id, city_id, branch_id),
                "concerns": self._get_top_concers(),
                "strength": self._get_opportunity_analysis(date_from_str, date_to_str, region_id, city_id, branch_id),
                "customer_analysis": self._get_customer_analysis(date_from_str, date_to_str, region_id, city_id, branch_id),
                "recommendation_analysis": self._get_recommendation_analysis(date_from_str, date_to_str, region_id, city_id, branch_id),
            }

            return Response(response_json(True, data, None))

        except Exception as e:
            return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))