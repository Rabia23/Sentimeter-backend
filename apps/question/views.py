from rest_framework.response import Response
from rest_framework.views import APIView
from apps.option.utils import option_get, get_related_option
from apps.question.models import Question
from apps.question.serializers import QuestionSerializer
from apps import constants
from apps.utils import save, response, response_json, get_param, get_data_param
from django.db import transaction


class QuestionView(APIView):
    def get(self, request, format=None):
        genre_type = get_param(request, 'genre_type', None)

        if genre_type:
            questions = Question.objects.filter(genreType=genre_type)
        else:
            questions = Question.objects.all()
        data = [question.to_dict() for question in questions]
        return Response(response_json(True, data, None))

    @transaction.atomic
    def post(self, request, format=None):
        text = get_data_param(request, 'text', None)

        question = Question.get_if_exists_by_text(text)
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response_json(True, serializer.data, None))
        return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))