from apps.review.models import Concern, Feedback

__author__ = 'aamish'

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        list = [{"keyword": concern.keyword, "count": 0} for concern in Concern.get_all_concerns()]

        for feedback in Feedback.manager.date("2016-03-01", "2016-03-31"):
        # for feedback in Feedback.objects.all():
            if feedback.comment_exists():
                for concern in list:
                    if feedback.comment.lower().find(concern["concern"]) != -1:
                        concern["count"] += 1

        for concern in list:
            self.stdout.write("keyword: " + concern["keyword"] + " - count: " + str(concern["count"]))