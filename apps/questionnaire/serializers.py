from rest_framework import serializers
from apps.questionnaire.models import Questionnaire


class QuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = ('id', 'title', 'isActive', 'branch')
