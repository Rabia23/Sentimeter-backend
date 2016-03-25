from rest_framework import serializers
from apps.question.models import Question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'text', 'isActive', 'type', 'objectId', 'genreType', 'promotion', 'questionnaire', 'image',
                  'text_urdu')
