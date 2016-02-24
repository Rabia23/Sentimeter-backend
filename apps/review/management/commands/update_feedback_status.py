from apps.review.models import Concern, Feedback

__author__ = 'aamish'

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):

        for feedback in Feedback.objects.all():
            feedback.mark_feedback_status()

        self.stdout.write("Successfully updated all feedback statuses")