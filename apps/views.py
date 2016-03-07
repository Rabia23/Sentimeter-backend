from django.contrib.auth import authenticate
from django.db.models import Count
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.area.models import Area
from apps.branch.models import Branch
from apps.city.models import City
from apps.option.models import Option
from apps.option.utils import generate_missing_options, generate_missing_sub_options, generate_option_groups, \
    generate_segmentation_with_options, generate_segmentation
from apps.person.enum import UserRolesEnum
from apps.person.models import UserInfo
from apps.promotion.models import Promotion
from apps.promotion.serializers import PromotionSerializer
from apps.question.models import Question
from apps.questionnaire.models import Questionnaire
from apps.questionnaire.serializers import QuestionnaireSerializer
from apps.region.models import Region
from apps.review.models import FeedbackOption, Feedback, Concern
from apps.review.serializers import FeedbackSerializer, FeedbackSearchSerializer
from apps.review.utils import generate_missing_actions, valid_action_id
from apps.serializers import ObjectSerializer, FeedbackCommentSerializer
from apps import constants
from dateutil import rrule
from dateutil.relativedelta import relativedelta
from django.core.paginator import Paginator
from django.utils import timezone
from operator import itemgetter
from apps.decorators import my_login_required
from apps.utils import get_param, get_data_param, get_user_data, get_user_role, response_json, get_next_day
from django.utils.decorators import method_decorator
from datetime import datetime, timedelta
from apps import constants
from rest_framework.mixins import ListModelMixin
from drf_haystack.generics import HaystackGenericAPIView


class LoginView(APIView):

    def post(self, request, format=None):
        username = get_data_param(request, 'username', None)
        password = get_data_param(request, 'password', None)
        user = authenticate(username=username, password=password)
        if user:
            if not user.info.first():
                return Response(response_json(False, None, 'User has no permission to login'))
            elif user.info.first() and not user.info.first().has_permission():
                return Response(response_json(False, None, 'User has no permission to login'))
            else:
                token = Token.objects.get_or_create(user=user)
                data = {'token': token[0].key,
                        'user': user.info.first().to_dict()}
                return Response(response_json(True, data, None))
        else:
            return Response(response_json(False, None, 'User not authenticated'))


class OverallFeedbackView(APIView):

    @method_decorator(my_login_required)
    def get(self, request, user, format=None):
        now = datetime.now()

        try:
            region_id, city_id, branch_id = get_user_data(user)

            date_to = get_param(request, 'date_to', str(now.date()))
            date_from = get_param(request, 'date_from', str((now - timedelta(days=1)).date()))

            feedback_options = FeedbackOption.manager.question(constants.TYPE_1).\
                                            date(date_from, date_to).filters(region_id, city_id, branch_id)
            feedback_options_dict = feedback_options.values('option_id', 'option__text', 'option__parent_id', 'option__score').\
                annotate(count=Count('option_id'))
            list_feedback = generate_missing_options(Question.objects.get(type=constants.TYPE_1), feedback_options_dict)

            data = {'feedback_count': feedback_options.count(), 'feedbacks': sorted(list_feedback, reverse=True, key=itemgetter('option__score'))}
            return Response(response_json(True, data, None))

        except Exception as e:
            return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))


class FeedbackAnalysisView(APIView):

    @method_decorator(my_login_required)
    def get(self, request, user, format=None):
        now = datetime.now()
        feedbacks = []
        objects = None

        try:
            type = get_param(request, 'type', None)
            question_type = get_param(request, 'question_type', constants.TYPE_1)

            date_to = get_param(request, 'date_to', str(now.date()))
            date_from = get_param(request, 'date_from', str((now - timedelta(days=1)).date()))

            feedback_options = FeedbackOption.manager.question(question_type).date(date_from, date_to)

            if type == constants.CITY_ANALYSIS:
                region_id = get_param(request, 'region', None)
                if region_id:
                    region = Region.objects.get(pk=region_id)
                    objects = region.cities.all()
            elif type == constants.BRANCH_ANALYSIS:
                city_id = get_param(request, 'city', None)
                if city_id:
                    city = City.objects.get(pk=city_id)
                    objects = city.branches.all()
            elif type == constants.REGIONAL_ANALYSIS:
                area_id = get_param(request, 'area', None)
                if area_id:
                    area = Area.objects.get(pk=area_id)
                    objects = area.regions.all()
                else:
                    objects = Region.objects.all()
            else:
                role = get_user_role(user)
                user_region_id, user_city_id, user_branch_id = get_user_data(user)
                if role == UserRolesEnum.OPERATIONAL_CONSULTANT:
                    objects = Region.objects.filter(id=user_region_id)
                    type = constants.REGIONAL_ANALYSIS
                elif role == UserRolesEnum.BRANCH_MANAGER:
                    objects = Branch.objects.filter(id=user_branch_id)
                    type = constants.BRANCH_ANALYSIS
                else:
                    objects = Area.objects.all()

            for object in objects:
                related_feedback_options = feedback_options.related_filters(type, object)
                filtered_feedback_options = related_feedback_options.values(
                    'option_id', 'option__text', 'option__parent_id').annotate(count=Count('option_id'))
                list_feedback = generate_missing_options(Question.objects.get(type=question_type), filtered_feedback_options)

                data = {'feedback_count': related_feedback_options.count(), 'feedbacks': list_feedback}
                feedbacks.append({'object': ObjectSerializer(object).data, 'data': data})

            feedback_data = {'count': objects.count(), 'analysis': feedbacks}
            return Response(response_json(True, feedback_data, None))

        except Exception as e:
            return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))


class FeedbackAnalysisBreakdownView(APIView):

    @method_decorator(my_login_required)
    def get(self, request, user, format=None):
        now = datetime.now()

        try:
            region_id = get_param(request, 'region', None)
            city_id = get_param(request, 'city', None)
            branch_id = get_param(request, 'branch', None)
            area_id = get_param(request, 'area', None)

            date_to = get_param(request, 'date_to', str(now.date()))
            date_from = get_param(request, 'date_from', str((now - timedelta(days=1)).date()))

            option_id = get_param(request, 'option', None)
            option = Option.objects.get(id=option_id)
            if option.is_parent():
                feedback_options = FeedbackOption.manager.children(option).feedback(option).\
                                        filters(region_id, city_id, branch_id, area_id).date(date_from, date_to)
                list_feedback = feedback_options.values('option_id', 'option__text', 'option__parent_id').\
                    annotate(count=Count('option_id'))

                data = {'feedback_count': feedback_options.count(), 'feedbacks': list_feedback}
                return Response(response_json(True, data, None))

            return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))
        except Exception as e:
            return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))


class OverallRatingView(APIView):

    @method_decorator(my_login_required)
    def get(self, request, user, format=None):
        feedback_records_list = []
        type = 0

        try:
            region_id, city_id, branch_id = get_user_data(user)

            option_id = get_param(request, 'option', None)
            option = Option.objects.get(id=option_id) if option_id else None

            question = Question.objects.get(type=constants.TYPE_2)

            date_to = get_param(request, 'date_to', None)
            date_from = get_param(request, 'date_from', None)

            current_tz = timezone.get_current_timezone()
            now = datetime.now()

            if date_to and date_from:
                current_tz = timezone.get_current_timezone()
                date_start = current_tz.localize(datetime.strptime(date_from + " 00:00:00", constants.DATE_FORMAT))
                date_end = current_tz.localize(datetime.strptime(date_to + " 23:59:59", constants.DATE_FORMAT))

                delta = date_end - date_start
                if delta.days >= constants.YEARLY_DAYS_COUNT:
                    rule = rrule.YEARLY
                elif delta.days >= constants.MONTHLY_DAYS_COUNT:
                    rule = rrule.MONTHLY
                elif delta.days >= constants.WEEKLY_DAYS_COUNT:
                    rule = rrule.WEEKLY
                else:
                    type = constants.DAILY_ANALYSIS
                    rule = rrule.DAILY
            else:
                date_to = str(now.date())
                rule = rrule.DAILY
                type = constants.DAILY_ANALYSIS
                date_from = str((now - timedelta(days=constants.NO_OF_DAYS - 1)).date())

            date_from = current_tz.localize(datetime.strptime(date_from + " 00:00:00", constants.DATE_FORMAT))
            date_to = current_tz.localize(datetime.strptime(date_to + " 23:59:59", constants.DATE_FORMAT))

            section_start_date = str(date_from.date())
            for single_date in rrule.rrule(rule, dtstart=date_from, until=date_to):
                if type != constants.DAILY_ANALYSIS:
                    section_end_date = str(single_date.date())
                    feedback_options = FeedbackOption.manager.date(section_start_date, section_end_date).\
                                        filters(region_id, city_id, branch_id)
                    section_start_date = str((single_date.date() + timedelta(days=1)))
                else:
                    feedback_options = FeedbackOption.manager.date(str(single_date.date()), str(single_date.date())).\
                                        filters(region_id, city_id, branch_id)

                feedback_options = feedback_options.children(option) if option else feedback_options.\
                                        question_parent_options(question)
                filtered_feedback = feedback_options.values('option_id', 'option__text', 'option__parent_id').\
                                        annotate(count=Count('option_id'))
                list_feedback = generate_missing_sub_options(option_id, filtered_feedback) if option else \
                                    generate_missing_options(question, filtered_feedback)

                date_data = {'feedback_count': feedback_options.count(), 'feedbacks': list_feedback}
                feedback_records_list.append({'date': single_date.date(), 'data': date_data})

            # if len(feedback_records_list) > constants.NO_OF_DAYS:
            #     feedback_records_list = feedback_records_list[-constants.NO_OF_DAYS:]

            return Response(response_json(True, feedback_records_list, None))

        except Exception as e:
            return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))


class CategoryPerformanceView(APIView):

    @method_decorator(my_login_required)
    def get(self, request, user, format=None):
        now = datetime.now()

        try:
            region_id, city_id, branch_id = get_user_data(user)

            date_to = get_param(request, 'date_to', str(now.date()))
            date_from = get_param(request, 'date_from', str((now - timedelta(days=1)).date()))

            option_id = get_param(request, 'option', None)
            option = Option.objects.get(id=option_id) if option_id else None
            question = Question.objects.get(type=constants.TYPE_2)

            if option:
                feedback_options = FeedbackOption.manager.children(option).date(date_from, date_to).\
                                                filters(region_id, city_id, branch_id)
            else:
                feedback_options = FeedbackOption.manager.question_parent_options(question).\
                                                date(date_from, date_to).filters(region_id, city_id, branch_id)

            filtered_feedback_options = feedback_options.values('option_id', 'option__text', 'option__parent_id').\
                                            annotate(count=Count('option_id'))
            list_feedback = generate_missing_sub_options(option_id, filtered_feedback_options) if option else \
                                generate_missing_options(question, filtered_feedback_options)

            data = {'feedback_count': feedback_options.count(), 'feedbacks': list_feedback}
            return Response(response_json(True, data, None))

        except Exception as e:
            return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))


class PositiveNegativeFeedbackView(APIView):

    @method_decorator(my_login_required)
    def get(self, request, user, format=None):
        try:
            region_id, city_id, branch_id = get_user_data(user)

            feedback = Feedback.manager.filters(region_id, city_id, branch_id)

            negative_feedback = feedback.top_comments(constants.NEGATIVE_SCORE_LIST)
            positive_feedback = feedback.top_comments(constants.POSITIVE_SCORE_LIST)

            data = {'positive_feedbacks': FeedbackSerializer(positive_feedback, many=True).data,
                    'negative_feedbacks': FeedbackSerializer(negative_feedback, many=True).data}
            return Response(response_json(True, data, None))

        except Exception as e:
            return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))


class CommentsView(APIView):

    @method_decorator(my_login_required)
    def get(self, request, user, format=None, *args, **kwargs):
        region_id, city_id, branch_id = get_user_data(user)
        page = int(get_param(request, 'page', 1))

        feedback = Feedback.manager.filters(region_id, city_id, branch_id).comments()
        paginator = Paginator(feedback, constants.COMMENTS_PER_PAGE)

        feedback_comments = [feedback.feedback_comment_dict() for feedback in paginator.page(page)]

        data = {'feedback_count': feedback.count(),
                'feedbacks': feedback_comments,
                'is_last_page': paginator.num_pages == int(page)}
        return Response(response_json(True, data, None))


class CommentsTextSearchView(ListModelMixin, HaystackGenericAPIView):

    serializer_class = FeedbackSearchSerializer

    @method_decorator(my_login_required)
    def get(self, request, user, format=None, *args, **kwargs):
        region_id, city_id, branch_id = get_user_data(user)

        elements = self.list(request, *args, **kwargs)

        id_list = [element["id"] for element in elements.data['results']]

        feedback = Feedback.objects.filter(id__in=id_list)

        feedback_comments = [feedback.feedback_comment_dict() for feedback in feedback]

        data = {'feedback_count': feedback.count(),
                'feedbacks': feedback_comments,
                'is_last_page': False}
        return Response(response_json(True, data, None))


class MapView(APIView):

    @method_decorator(my_login_required)
    def get(self, request, user, format=None):
        now = datetime.now()

        try:
            region_id, city_id, branch_id = get_user_data(user)

            date_to = get_param(request, 'date_to', str(now.date()))
            date_from = get_param(request, 'date_from', str((now - timedelta(days=1)).date()))

            if region_id:
                branches = Branch.objects.filter(city__region__exact=region_id)
            elif branch_id:
                branches = Branch.objects.filter(id=branch_id)
            else:
                branches = Branch.objects.all()

            branch_detail_list = [branch.branch_feedback_detail(date_from, date_to) for branch in branches]

            data = {'branch_count': branches.count(), 'branches': branch_detail_list}
            return Response(response_json(True, data, None))

        except Exception as e:
            return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))


class FeedbackSegmentationView(APIView):

    @method_decorator(my_login_required)
    def get(self, request, user, format=None):
        try:
            region_id, city_id, branch_id = get_user_data(user)
            type = get_param(request, 'type', None)

            option_id = get_param(request, 'option', None)
            option = Option.objects.get(id=option_id) if option_id else None

            date_to = get_param(request, 'date_to', None)
            date_to = datetime.strptime(date_to, constants.ONLY_DATE_FORMAT_02).date()

            if option:
                options = option.children.all()
            else:
                return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))

            if type == constants.YEARLY_ANALYSIS:
                date_from = str((date_to - relativedelta(months=constants.NO_OF_MONTHS)))
            elif type == constants.MONTHLY_ANALYSIS:
                date_from = str((date_to - relativedelta(weeks=constants.NO_OF_WEEKS)))
            elif type == constants.WEEK_ANALYSIS:
                date_from = str((date_to - timedelta(days=constants.NO_OF_DAYS)))
            else:
                date_from = str(date_to)

            date_to = str(date_to)

            feedback_options = FeedbackOption.manager.children(option).date(date_from, date_to).filters(region_id, city_id, branch_id)
            feedback_segmented_list = generate_option_groups(feedback_options, options)

            data = {'option_count': len(feedback_segmented_list), 'options': feedback_segmented_list}
            return Response(response_json(True, data, None))

        except Exception as e:
            return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))


class TopConcernsView(APIView):

    @method_decorator(my_login_required)
    def get(self, request, user, format=None):
        try:
            concerns = [concern.to_dict() for concern in Concern.objects.filter(is_active=True).order_by("-count")[:5]]
            data = {'concern_count': len(concerns), 'concern_list': concerns}

            return Response(response_json(True, data, None))
        except Exception as e:
            return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))


class SegmentationRatingView(APIView):

    @method_decorator(my_login_required)
    def get(self, request, user, format=None):
        now = datetime.now()
        try:
            region_id, city_id, branch_id = get_user_data(user)

            option_id = get_param(request, 'option', None)
            option = Option.objects.get(id=option_id) if option_id else None

            date_to = get_param(request, 'date_to', str(now.date()))
            date_from = get_param(request, 'date_from', str((now - timedelta(days=1)).date()))

            question = Question.objects.get(type=constants.TYPE_2)

            options = option.children.all() if option else question.options.all()
            feedback_options = FeedbackOption.manager.options(options).date(date_from, date_to).\
                                    filters(region_id, city_id, branch_id)

            feedback_segmented_list = generate_segmentation_with_options(feedback_options, options)

            data = {'segment_count': len(feedback_segmented_list), 'segments': feedback_segmented_list}
            return Response(response_json(True, data, None))

        except Exception as e:
            return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))


class ActionTakenView(APIView):

    @method_decorator(my_login_required)
    def post(self, request, user, format=None):
        try:
            feedback_id = get_data_param(request, 'feedback_id', None)
            action_id = get_data_param(request, 'action_id', None)

            action_id = int(action_id) if action_id else None
            if feedback_id and action_id and valid_action_id(action_id):
                feedback = Feedback.objects.get(pk=feedback_id)

                feedback.updated_at = datetime.now()
                feedback.action_taken = action_id
                feedback.save()

                return Response(response_json(True, feedback.feedback_comment_dict(), None))
            else:
                return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))
        except Exception as e:
            return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))


class ActionAnalysisView(APIView):

    @method_decorator(my_login_required)
    def get(self, request, user, format=None):
        now = datetime.now()
        data_list = []
        objects = None

        try:
            type = get_param(request, 'type', None)

            date_to = get_param(request, 'date_to', str(now.date()))
            date_from = get_param(request, 'date_from', str((now - timedelta(days=1)).date()))

            if type == constants.CITY_ANALYSIS:
                region_id = get_param(request, 'region', None)
                if region_id:
                    region = Region.objects.get(pk=region_id)
                    objects = region.cities.all()
            elif type == constants.BRANCH_ANALYSIS:
                city_id = get_param(request, 'city', None)
                if city_id:
                    city = City.objects.get(pk=city_id)
                    objects = city.branches.all()
            elif type == constants.REGIONAL_ANALYSIS:
                area_id = get_param(request, 'area', None)
                if area_id:
                    area = Area.objects.get(pk=area_id)
                    objects = area.regions.all()
                else:
                    objects = Region.objects.all()
            else:
                role = get_user_role(user)
                user_region_id, user_city_id, user_branch_id = get_user_data(user)
                if role == UserRolesEnum.OPERATIONAL_CONSULTANT:
                    objects = Region.objects.filter(id=user_region_id)
                    type = constants.REGIONAL_ANALYSIS
                elif role == UserRolesEnum.BRANCH_MANAGER:
                    objects = Branch.objects.filter(id=user_branch_id)
                    type = constants.BRANCH_ANALYSIS
                else:
                    objects = Area.objects.all()

            for object in objects:
                feedback = Feedback.manager.related_filters(type, object).date(date_from, date_to)
                filtered_feedback = feedback.values('action_taken').annotate(count=Count('action_taken'))
                filtered_feedback = generate_missing_actions(filtered_feedback)

                data = {'feedback_count': feedback.count(), 'action_analysis': filtered_feedback}
                data_list.append({'object': ObjectSerializer(object).data, 'data': data})

            feedback_data = {'count': objects.count(), 'analysis': data_list}
            return Response(response_json(True, feedback_data, None))

        except Exception as e:
            return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))


class TopChartsView(APIView):

    @method_decorator(my_login_required)
    def get(self, request, user, format=None):
        try:

            now = datetime.now()

            date_to_str = str(now.date())
            date_from_str = str((now - timedelta(days=1)).date())

            branch = Feedback.get_top_branch(date_from_str, date_to_str)
            city = Feedback.get_top_city(date_from_str, date_to_str)
            region = Feedback.get_top_region(date_from_str, date_to_str)
            gro = Feedback.get_top_gro(date_from_str, date_to_str)
            
            data = {'branch': branch, 'city': city, 'region': region, 'gro': gro}
            return Response(response_json(True, data, None))
            
        except Exception as e:
            return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))


#for live dashboard
class TopRankingsView(APIView):

    @method_decorator(my_login_required)
    def get(self, request, user, format=None):
        try:
            overall_experience = FeedbackOption.get_top_option()
            positive_negative_feedback = Feedback.get_feedback_type_count()
            qsc_count = FeedbackOption.get_qsc_count()

            data = {'overall_experience': overall_experience,
                    'top_concern': "Ketchup",
                    'positive_negative_feedback': positive_negative_feedback,
                    'qsc_count': qsc_count}

            return Response(response_json(True, data, None))

        except Exception as e:
            return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))


#for live dashboard
class ComplaintAnalysisView(APIView):

    @method_decorator(my_login_required)
    def get(self, request, user, format=None):
        try:
            data_list = []
            objects = Area.objects.all()

            feedback = Feedback.manager.normal_feedback()
            filtered_feedback = feedback.values('action_taken').annotate(count=Count('action_taken'))
            filtered_feedback = generate_missing_actions(filtered_feedback)

            data = {'feedback_count': feedback.count(), 'action_analysis': filtered_feedback}
            data_list.append({'object': {"id": "", "name": "Pakistan", "objectId": ""}, 'data': data})

            for object in objects:
                feedback = Feedback.manager.related_filters(0, object).normal_feedback()
                filtered_feedback = feedback.values('action_taken').annotate(count=Count('action_taken'))
                filtered_feedback = generate_missing_actions(filtered_feedback)

                data = {'feedback_count': feedback.count(), 'action_analysis': filtered_feedback}
                data_list.append({'object': ObjectSerializer(object).data, 'data': data})

            return Response(response_json(True, data_list, None))

        except Exception as e:
            return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))


#for live dashboard
class LeaderBoardView(APIView):

    @method_decorator(my_login_required)
    def get(self, request, user, format=None):
        try:
            city = Feedback.get_top_city()
            branches = Feedback.get_top_branches()
            gro = Feedback.get_top_gro()

            data = {'city': city, "branches": branches, "gro": gro}
            return Response(response_json(True, data, None))

        except Exception as e:
            return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))


class LiveDashboardView(APIView):

    def _get_complaint_view(self, date_from, date_to):
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

    def _get_top_concers(self):
        concerns = [concern.to_dict() for concern in Concern.objects.filter(is_active=True).order_by("-count")[:5]]
        return {'concern_count': len(concerns), 'concern_list': concerns}

    def _get_top_segment(self, date_from, date_to):
        question = Question.objects.get(type=constants.TYPE_1)

        options = question.options.all()
        feedback_options = FeedbackOption.manager.options(options).date(date_from, date_to)

        feedback_segmented_list = generate_segmentation(feedback_options)
        feedback_segmented_counts = [segment["option_count"] for segment in feedback_segmented_list]
        return feedback_segmented_list[feedback_segmented_counts.index(max(feedback_segmented_counts))]

    def _get_overall_feedback(self, date_from, date_to):
        feedback_options = FeedbackOption.manager.question(constants.TYPE_1).date(date_from, date_to)
        feedback_options_dict = feedback_options.values('option_id', 'option__text', 'option__parent_id', 'option__score').\
            annotate(count=Count('option_id'))
        list_feedback = generate_missing_options(Question.objects.get(type=constants.TYPE_1), feedback_options_dict)

        return {'feedback_count': feedback_options.count(), 'feedbacks': sorted(list_feedback, reverse=True, key=itemgetter('option__score'))}

    def _get_segmentation_rating(self, date_from, date_to):
        question = Question.objects.get(type=constants.TYPE_2)

        options = question.options.all()
        feedback_options = FeedbackOption.manager.options(question.options.all()).date(date_from, date_to)

        feedback_segmented_list = generate_segmentation_with_options(feedback_options, options)

        return {'segment_count': len(feedback_segmented_list), 'segments': feedback_segmented_list}

    def _get_top_rankings(self, date_from=None, date_to=None):
        overall_experience = FeedbackOption.get_top_option(date_from, date_to)
        positive_negative_feedback = Feedback.get_feedback_type_count(date_from, date_to)
        qsc_count = FeedbackOption.get_qsc_count(date_from, date_to)

        return {'overall_experience': overall_experience,
                'top_segment': self._get_top_segment(date_from, date_to),
                'positive_negative_feedback': positive_negative_feedback,
                'qsc_count': qsc_count}

    def _get_leaderboard_view(self, date_from, date_to):
        city = Feedback.get_top_city(date_from, date_to)
        branches = Feedback.get_top_branches(date_from, date_to)
        gro = Feedback.get_top_gro(date_from, date_to)

        return {'city': city, "branches": branches, "gro": gro}

    def _get_overall_rating(self, date_from, date_to):
        feedback_records_list = []

        current_tz = timezone.get_current_timezone()
        date_from = current_tz.localize(datetime.strptime(date_from + " 00:00:00", constants.DATE_FORMAT))
        date_to = current_tz.localize(datetime.strptime(date_to + " 23:59:59", constants.DATE_FORMAT))

        rule = rrule.DAILY
        question = Question.objects.get(type=constants.TYPE_2)
        for single_date in rrule.rrule(rule, dtstart=date_from, until=date_to):
            feedback_options = FeedbackOption.manager.date(str(single_date.date()), str(single_date.date()))
            feedback_options = feedback_options.question_parent_options(question)
            filtered_feedback = feedback_options.values('option_id', 'option__text', 'option__parent_id').\
                                    annotate(count=Count('option_id'))
            list_feedback = generate_missing_options(question, filtered_feedback)

            date_data = {'feedback_count': feedback_options.count(), 'feedbacks': list_feedback}
            feedback_records_list.append({'date': single_date.date(), 'data': date_data})

        if len(feedback_records_list) > constants.NO_OF_DAYS:
            feedback_records_list = feedback_records_list[-constants.NO_OF_DAYS:]

        return feedback_records_list

    def _get_opportunity_analysis(self, date_from, date_to):
        feedback_options = FeedbackOption.manager.question(constants.TYPE_3).date(date_from, date_to)
        feedback_options_dict = feedback_options.values('option_id', 'option__text', 'option__parent_id', 'option__score').\
                annotate(count=Count('option_id'))

        list_feedback = generate_missing_options(Question.objects.get(type=constants.TYPE_3), feedback_options_dict)
        return {'feedback_count': feedback_options.count(), 'feedbacks': list_feedback}

    @method_decorator(my_login_required)
    def get(self, request, user, format=None):
        try:
            now = datetime.now()

            date_to_str = str(now.date())
            date_from_str = str((now - timedelta(days=1)).date())

            data = {
                "segmentation_rating": self._get_segmentation_rating(date_from_str, date_to_str),
                "overall_feedback": self._get_overall_feedback(date_from_str, date_to_str),
                "overall_rating": self._get_overall_rating(str((now - timedelta(days=constants.NO_OF_DAYS)).date()), date_to_str),
                "complaint_view": self._get_complaint_view(date_from_str, date_to_str),
                "top_rankings": self._get_top_rankings(date_from_str, date_to_str),
                "leaderboard_view": self._get_leaderboard_view(date_from_str, date_to_str),
                "concerns": self._get_top_concers(),
                "strength": self._get_opportunity_analysis(date_from_str, date_to_str),
            }

            return Response(response_json(True, data, None))

        except Exception as e:
            return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))


class ManageUserView(APIView):

    @method_decorator(my_login_required)
    def get(self, request, user, format=None):
        people = []
        child_role = None
        parent = user.info.first()

        if not parent:
            return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))

        parent_role = user.info.first().role

        #can be refactored more
        if parent_role == UserRolesEnum.BRANCH_MANAGER:
            people = UserInfo.get_children_dict(UserRolesEnum.GRO, UserRolesEnum.BRANCH_MANAGER, user.id)
            child_role = UserRolesEnum.GRO
        elif parent_role == UserRolesEnum.OPERATIONAL_CONSULTANT:
            people = UserInfo.get_children_dict(UserRolesEnum.BRANCH_MANAGER, UserRolesEnum.OPERATIONAL_CONSULTANT, user.id)
            child_role = UserRolesEnum.BRANCH_MANAGER
        elif parent_role == UserRolesEnum.OPERATIONAL_MANAGER:
            people = UserInfo.get_children_dict(UserRolesEnum.OPERATIONAL_CONSULTANT, UserRolesEnum.OPERATIONAL_MANAGER, user.id)
            child_role = UserRolesEnum.OPERATIONAL_CONSULTANT
        elif parent_role == UserRolesEnum.ASSISTANT_DIRECTOR:
            people = UserInfo.get_children_dict(UserRolesEnum.OPERATIONAL_MANAGER, UserRolesEnum.ASSISTANT_DIRECTOR, user.id)
            child_role = UserRolesEnum.OPERATIONAL_MANAGER
        elif parent_role == UserRolesEnum.DIRECTOR:
            people = UserInfo.get_children_dict(UserRolesEnum.ASSISTANT_DIRECTOR, UserRolesEnum.DIRECTOR, user.id)
            child_role = UserRolesEnum.ASSISTANT_DIRECTOR

        data = {
            "parent": user.info.first().to_dict(),
            "parent_role": parent_role,
            "parent_id": user.id,
            "child_role": child_role,
            "children": people,
        }

        return Response(response_json(True, data, None))


class OpportunityAnalysisView(APIView):

    @method_decorator(my_login_required)
    def get(self, request, user, format=None):
        now = datetime.now()

        try:
            region_id, city_id, branch_id = get_user_data(user)

            date_to = get_param(request, 'date_to', str(now.date()))
            date_from = get_param(request, 'date_from', str((now - timedelta(days=1)).date()))

            feedback_options = FeedbackOption.manager.question(constants.TYPE_3).date(date_from, date_to).\
                filters(region_id, city_id, branch_id)
            feedback_options_dict = feedback_options.values('option_id', 'option__text', 'option__parent_id', 'option__score').\
                annotate(count=Count('option_id'))

            list_feedback = generate_missing_options(Question.objects.get(type=constants.TYPE_3), feedback_options_dict)

            data = {'feedback_count': feedback_options.count(), 'feedbacks': list_feedback}
            return Response(response_json(True, data, None))

        except Exception as e:
            return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))


class PromotionDetailView(APIView):

    @method_decorator(my_login_required)
    def get(self, request, user, format=None):
        now = datetime.now()

        try:
            region_id, city_id, branch_id = get_user_data(user)
            id = get_param(request, 'id', None)

            date_to = get_param(request, 'date_to', str(now.date()))
            date_from = get_param(request, 'date_from', str((now - timedelta(days=1)).date()))

            promotion = Promotion.objects.get(pk=id)
            questions = promotion.questions.all().order_by("-created_at")

            question_data_list = []
            for question in questions:
                total_count = 0
                feedback_options = FeedbackOption.manager.promotion_options(question).\
                    filters(region_id, city_id, branch_id).date(date_from, date_to)
                filtered_feedback = feedback_options.values('option_id', 'option__text', 'option__parent_id', 'option__score').\
                                    annotate(count=Count('option_id'))
                list_feedback = generate_missing_options(question, filtered_feedback)
                for feedback_count in list_feedback:
                    total_count += int(feedback_count["count"])
                question_data_list.append({'question': question.text, 'total_count': total_count, 'type': question.type, 'feedbacks': list_feedback})

            data = {'question': questions.count(), 'promotion': PromotionSerializer(promotion).data, 'analysis': question_data_list}
            return Response(response_json(True, data, None))

        except Promotion.DoesNotExist as e:
            return Response(response_json(False, None, constants.TEXT_DOES_NOT_EXISTS))
        except Exception as e:
            return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))


class QuestionnaireDetailView(APIView):
    
    @method_decorator(my_login_required)
    def get(self, request, user, format=None):
        now = datetime.now()

        try:
            region_id, city_id, branch_id = get_user_data(user)
            id = get_param(request, 'id', None)

            date_to = get_param(request, 'date_to', str(now.date()))
            date_from = get_param(request, 'date_from', str((now - timedelta(days=1)).date()))

            questionnaire = Questionnaire.objects.get(pk=id)
            questions = questionnaire.questions.all().order_by("created_at")

            question_data_list = []
            for question in questions:
                total_count = 0
                feedback_options = FeedbackOption.manager.promotion_options(question).\
                    filters(region_id, city_id, branch_id).date(date_from, date_to)
                filtered_feedback = feedback_options.values('option_id', 'option__text', 'option__parent_id', 'option__score').\
                                    annotate(count=Count('option_id'))
                list_feedback = generate_missing_options(question, filtered_feedback)
                for feedback_count in list_feedback:
                    total_count += int(feedback_count["count"])
                question_data_list.append({'question': question.text, 'total_count': total_count, 'type': question.type, 'feedbacks': list_feedback})

            data = {'question': questions.count(), 'questionnaire': QuestionnaireSerializer(questionnaire).data, 'analysis': question_data_list}
            return Response(response_json(True, data, None))

        except Questionnaire.DoesNotExist as e:
            return Response(response_json(False, None, constants.TEXT_DOES_NOT_EXISTS))
        except Exception as e:
            return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))


class CommentsSearchView(APIView):

    # @method_decorator(my_login_required)
    def get(self, request, format=None):
        try:
            text = get_param(request, 'text', None)
            all_results = Feedback.objects.filter(comment__icontains=text)

            data = [result.feedback_comment_dict() for result in all_results]
            return Response(response_json(True, data, None))
        except Exception as e:
            return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))



