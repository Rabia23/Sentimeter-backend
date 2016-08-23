__author__ = 'rabia'
from apps.area.models import Area
from django.contrib.auth.models import User
from apps.question.models import Question
from apps.promotion.models import Promotion
from apps.questionnaire.models import Questionnaire
from apps.review.models import Feedback
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        Area.objects.all().delete()
        self.stdout.write("data successfully deleted from area table.")
        self.stdout.write("data successfully deleted from region table.")
        self.stdout.write("data successfully deleted from city table.")
        self.stdout.write("data successfully deleted from branch table.")
        self.stdout.write("related branch users and region users data successfully deleted from UserInfo table.")
        self.stdout.write("related branch feedbacks successfully deleted from feedback and feedbackOption tables.")

        User.objects.all().delete()
        self.stdout.write("data successfully deleted from user table.")
        self.stdout.write("data successfully deleted from userInfo table.")

        Promotion.objects.all().delete()
        self.stdout.write("data successfully deleted from promotion table.")
        self.stdout.write("promotion related data successfully deleted from question table.")
        self.stdout.write("promotion related data successfully deleted from option table.")

        Questionnaire.objects.all().delete()
        self.stdout.write("data successfully deleted from questionnaire table.")
        self.stdout.write("questionnaire related data successfully deleted from question table.")
        self.stdout.write("questionnaire related data successfully deleted from option table.")

        Question.objects.all().delete()
        self.stdout.write("data successfully deleted from question table.")
        self.stdout.write("data successfully deleted from option table.")

        Feedback.objects.all().delete()
        self.stdout.write("data successfully deleted from feedback table.")
        self.stdout.write("data successfully deleted from feedbackOption table.")