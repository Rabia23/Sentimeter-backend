from apps.review.models import Concern, Feedback

__author__ = 'aamish'

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        list = [{"keyword": concern.keyword, "count": 0} for concern in Concern.get_all_concerns()]

        for feedback in Feedback.objects.all():
            if feedback.comment_exists() and feedback.is_negative():
                for concern in list:
                    if feedback.comment.lower().find(concern["keyword"]) != -1:
                        concern["count"] += 1

        for concern in list:
            Concern.objects.filter(keyword=concern["keyword"]).update(count=concern["count"])
            self.stdout.write("keyword: " + concern["keyword"] + " - count: " + str(concern["count"]))

        self.stdout.write("Successfully updated all keyword statuses")