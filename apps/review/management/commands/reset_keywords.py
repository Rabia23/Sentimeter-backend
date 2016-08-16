__author__ = 'rabia'
from apps.review.models import Concern
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        concerns = Concern.objects.all()
        if concerns:
            concerns.update(count=0)
            self.stdout.write("Successfully reset all keywords.")
        else:
            self.stdout.write("No keyword found!")