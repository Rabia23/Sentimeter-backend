import csv
from apps.review.models import Feedback

__author__ = 'aamish'

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):

        file = open('feedback.csv','w')
        try:
            writer = csv.writer(file)
            writer.writerow(('Feedback Id', 'Comment', 'Action Taken', 'GRO', 'Branch', 'Options'))
            for feedback in Feedback.objects.all():
                self.stdout.write("Feedback ID = " + str(feedback.id))
                writer.writerow((feedback.id,
                                 feedback.comment,
                                 feedback.action_taken,
                                 feedback.gro_name,
                                 feedback.branch.name,
                                 [str(feedback_option.option.text) for feedback_option in feedback.feedback_option.all()]))
        finally:
            file.close()

        self.stdout.write("Successfully Created")
