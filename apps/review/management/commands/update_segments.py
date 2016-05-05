from apps.review.models import Feedback

__author__ = 'aamish'

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):

        for feedback in Feedback.objects.all():
            feedback.mark_segment()

        self.stdout.write("Successfully updated all segments")