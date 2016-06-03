from apps.review.models import Feedback
from lively._celery import send_feedback_email_report

__author__ = 'aamish'

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):

        all_feedback = Feedback.objects.filter(is_emailed=False)
        feedback_comments = [feedback.feedback_comment_dict() for feedback in all_feedback]

        if all_feedback:
            send_feedback_email_report.delay(feedback_comments)
            all_feedback.update(is_emailed=True)
            self.stdout.write("Successfully Reported!")
        else:
            self.stdout.write("No Report Generated!")