from django.db.models import Count
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.area.models import Area
from apps.branch.models import Branch
from apps.option.utils import generate_missing_options, generate_missing_segments
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
from apps.region.models import Region
import logging
from lively import local_settings

logging.basicConfig(filename=local_settings.LOG_FILENAME, level=logging.ERROR, format='%(asctime)s %(levelname)s %(message)s',)


# Create your views here.
class ReportView(APIView):

    def _get_complaint_view(self, date_from, date_to, region_id, city_id, branch_id):
        data_list = []
        objects = Region.objects.all()

        for object in objects:
            feedback = Feedback.manager.related_filters(constants.REGIONAL_ANALYSIS, object).date(date_from, date_to)
            filtered_feedback = feedback.values('action_taken').annotate(count=Count('action_taken'))
            filtered_feedback = generate_missing_actions(filtered_feedback)

            data = {'feedback_count': feedback.count(), 'action_analysis': filtered_feedback}
            data_list.append({'object': ObjectSerializer(object).data, 'data': data})

        return {'count': objects.count(), 'analysis': data_list}

    def _get_top_concerns(self):
        concerns = [concern.to_dict() for concern in Concern.objects.filter(is_active=True).order_by("-count")[:5]]
        return {'concern_count': len(concerns), 'concern_list': concerns}

    def _get_overall_feedback(self, date_from, date_to, region_id, city_id, branch_id):
        feedback_options = FeedbackOption.manager.question(constants.TYPE_1).date(date_from, date_to).filters(region_id, city_id, branch_id)
        feedback_options_dict = feedback_options.values('option_id', 'option__text', 'option__parent_id', 'option__score', 'option__color_code').\
            annotate(count=Count('option_id'))
        list_feedback = generate_missing_options(Question.objects.get(type=constants.TYPE_1), feedback_options_dict)

        return {'feedback_count': feedback_options.count(), 'feedbacks': sorted(list_feedback, reverse=True, key=itemgetter('option__score'))}

    def _get_segments(self, date_from, date_to, region_id, city_id, branch_id):
        options_data = []
        question = Question.objects.get(type=constants.TYPE_2)
        options = question.options.all()
        feedback_options = FeedbackOption.manager.date(date_from, date_to).filters(region_id, city_id, branch_id)

        for option in options:
            sub_options_segments_list = []

            option_feedback = feedback_options.filter(option=option).values_list('feedback_id')
            segments_feedback = Feedback.objects.filter(id__in=option_feedback).values('segment').annotate(count=Count('segment'))

            for child_option in option.children.all():
                sub_option_feedback = feedback_options.filter(option=child_option).values_list('feedback_id')
                sub_option_segments_feedback = Feedback.objects.filter(id__in=sub_option_feedback).values('segment').annotate(count=Count('segment'))
                sub_options_segments_list.append({'option_name': child_option.text, 'segments': generate_missing_segments(sub_option_segments_feedback)})
            options_data.append({'option_object': option.to_object_dict(), 'segments': generate_missing_segments(segments_feedback), 'sub_option_segments': sub_options_segments_list})

        return options_data

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

    def _get_patch_analysis(self, date_from, date_to, region_id, city_id, branch_id):
        question_type = [constants.TYPE_1, constants.TYPE_2]
        region_objects = Region.objects.all()
        question_feedbacks = []

        for type in question_type:
            feedback_options = FeedbackOption.manager.question(type).date(date_from, date_to)
            feedbacks = []
            for object in region_objects:
                related_feedback_options = feedback_options.related_filters(constants.REGIONAL_ANALYSIS, object)
                filtered_feedback_options = related_feedback_options.values('option_id', 'option__text', 'option__parent_id', 'option__score', 'option__color_code').annotate(count=Count('option_id'))
                list_feedback = generate_missing_options(Question.objects.get(type=type), filtered_feedback_options)

                data = {'feedback_count': related_feedback_options.count(), 'feedbacks': sorted(list_feedback, reverse=True, key=itemgetter('option__score'))}
                feedbacks.append({'object': ObjectSerializer(object).data, 'data': data})
            question_feedbacks.append({'question_feedbacks': feedbacks})
        return {'count': region_objects.count(), 'analysis': question_feedbacks}

    def _get_benchmark_counts(self, date_from_str, date_to_str):
        branch_details = []
        branches = Branch.objects.all()

        current_tz = timezone.get_current_timezone()
        date_to = current_tz.localize(datetime.strptime(date_to_str + " 23:59:59", constants.DATE_FORMAT))
        date_from = current_tz.localize(datetime.strptime(date_from_str + " 00:00:00", constants.DATE_FORMAT))

        rule = rrule.DAILY
        for branch in branches:
            branch_detail_list = []
            total_feedback_count = 0
            for single_date in rrule.rrule(rule, dtstart=date_from, until=date_to):
                feedback_count = branch.get_branch_feedback_count(str(single_date.date()), str(single_date.date()))
                total_feedback_count += feedback_count
                branch_detail_list.append({
                    "date": str(single_date.date()),
                    "feedback_count": feedback_count,
                    "count_exceeded": feedback_count >= branch.benchmark_count,
                })
            branch_details.append({
                "id": branch.id,
                "name": branch.name,
                "latitude": branch.latitude,
                "longitude": branch.longitude,
                "city": branch.city.name,
                "region": branch.city.region.name,
                "total_feedback_count": total_feedback_count,
                "details": branch_detail_list,
            })
        return {'branch_count': branches.count(), 'branches_data': branch_details}

    @method_decorator(my_login_required)
    def get(self, request, user, format=None):
        try:
            now = datetime.now()
            region_id, city_id, branch_id = get_user_data(user)

            date_to_str = get_param(request, 'date_to', str(now.date()))
            date_from_str = get_param(request, 'date_from', str((now - timedelta(days=1)).date()))

            data = {
                "benchmark_analysis": self._get_benchmark_counts(date_from_str, date_to_str),
                "segmentation_rating": self._get_segments(date_from_str, date_to_str, region_id, city_id, branch_id),
                "overall_rating": self._get_overall_feedback(date_from_str, date_to_str, region_id, city_id, branch_id),
                "patch_analysis": self._get_patch_analysis(date_from_str, date_to_str, region_id, city_id, branch_id),
                "complaint_view": self._get_complaint_view(date_from_str, date_to_str, region_id, city_id, branch_id),
                "concerns": self._get_top_concerns(),
                "opportunity_analysis": self._get_opportunity_analysis(date_from_str, date_to_str, region_id, city_id, branch_id),
                "age_group_analysis": self._get_customer_analysis(date_from_str, date_to_str, region_id, city_id, branch_id),
                "recommendation_analysis": self._get_recommendation_analysis(date_from_str, date_to_str, region_id, city_id, branch_id)
            }

            return Response(response_json(True, data, None))

        except Exception as e:
            logging.exception("--------------------------------")
            return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))