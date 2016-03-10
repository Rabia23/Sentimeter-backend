import csv
from apps.review.models import Feedback

__author__ = 'aamish'

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):

        file = open('eggs.csv','w')
        try:
            writer = csv.writer(file)
            writer.writerow(('Feedback Id', 'Comment', 'Action Taken'))
            for feedback in Feedback.objects.all():
                writer.writerow((feedback.id, feedback.comment, feedback.action_taken))
        finally:
            file.close()

        self.stdout.write("Successfully Created")
