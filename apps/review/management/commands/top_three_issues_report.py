from apps.review.models import FeedbackOption
from apps.question.models import Question
from apps.branch.models import Branch
from apps.region.models import Region
from apps import constants
from django.db.models import Count
from apps.option.utils import generate_missing_sub_options
from operator import itemgetter
from lively.mailgun import sendTopIssuesReport
from datetime import datetime, timedelta

__author__ = 'rabia'

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def calculate_percentage(self, feedback_list, negative_feedbacks_count):

        for feedback in feedback_list:
            percentage = round((feedback['count']/negative_feedbacks_count)*100) if feedback['count'] > 0 else 0
            feedback['percentage'] = percentage if negative_feedbacks_count > 0 else 0

    def get_branches_list(self):

        branches_list = []

        now = datetime.now()
        date_from = str((now - timedelta(days=7)).date())
        date_to = str((now - timedelta(days=1)).date())

        negative_options = Question.objects.get(type=constants.TYPE_1).options.filter(score__in=constants.NEGATIVE_SCORE_LIST)
        options = Question.objects.get(type=constants.TYPE_2).options.all()

        for branch in Branch.objects.all():
            feedback_list = []
            negative_feedbacks = FeedbackOption.manager.negative_feedbacks(negative_options).date(date_from, date_to).filters("", "", branch.id)
            negative_feedbacks_count = negative_feedbacks.count()

            for option in options:
                feedback_options = FeedbackOption.manager.children(option).date(date_from, date_to).filters("", "", branch.id)
                filtered_feedback_options = feedback_options.values('option_id', 'option__text', 'option__parent_id', 'option__color_code', 'option__score').\
                                                annotate(count=Count('option_id'))
                list_feedback = generate_missing_sub_options(option, filtered_feedback_options)
                feedback_list.extend(list_feedback)

            feedback_list = sorted(feedback_list, key=itemgetter('count'), reverse=True)
            feedback_list = feedback_list[:3]
            self.calculate_percentage(feedback_list, negative_feedbacks_count)
            branches_list.append({"branch": branch.name, "negative_feedbacks_count": negative_feedbacks_count, "issues_list": feedback_list})
        return branches_list

    def get_patches_list(self):

        patches_list = []

        now = datetime.now()
        date_from = str((now - timedelta(days=7)).date())
        date_to = str((now - timedelta(days=1)).date())

        negative_options = Question.objects.get(type=constants.TYPE_1).options.filter(score__in=constants.NEGATIVE_SCORE_LIST)
        options = Question.objects.get(type=constants.TYPE_2).options.all()

        for region in Region.objects.all():
            feedback_list = []
            negative_feedbacks = FeedbackOption.manager.negative_feedbacks(negative_options).date(date_from, date_to).filters(region.id, "", "")
            negative_feedbacks_count = negative_feedbacks.count()

            for option in options:
                feedback_options = FeedbackOption.manager.children(option).date(date_from, date_to).filters(region.id, "", "")
                filtered_feedback_options = feedback_options.values('option_id', 'option__text', 'option__parent_id', 'option__color_code', 'option__score').\
                                                annotate(count=Count('option_id'))
                list_feedback = generate_missing_sub_options(option, filtered_feedback_options)
                feedback_list.extend(list_feedback)

            feedback_list = sorted(feedback_list, key=itemgetter('count'), reverse=True)
            feedback_list = feedback_list[:3]
            self.calculate_percentage(feedback_list, negative_feedbacks_count)
            patches_list.append({"patch": region.name, "negative_feedbacks_count": negative_feedbacks_count, "issues_list": feedback_list})
        return patches_list

    def handle(self, *args, **options):
        branches_list = self.get_branches_list()
        patches_list = self.get_patches_list()

        sendTopIssuesReport(branches_list, patches_list)

        print("branches list")
        print(branches_list)
        print("---------------------------------------------------------")
        print("patches list")
        print(patches_list)
