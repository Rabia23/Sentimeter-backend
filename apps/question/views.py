from rest_framework.response import Response
from rest_framework.views import APIView
from apps.option.utils import option_get, get_related_option
from apps.question.models import Question
from apps.question.serializers import QuestionSerializer
from apps import constants
from apps.utils import save, response, response_json, get_param, get_data_param
from django.db import transaction
import logging
from lively import local_settings

logging.basicConfig(filename=local_settings.LOG_FILENAME, level=logging.ERROR, format='%(asctime)s %(levelname)s %(message)s',)



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
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response_json(True, serializer.data, None))
        return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))

    @transaction.atomic
    def put(self, request, format=None):
        id = get_data_param(request, 'id', None)

        try:
            question = Question.objects.get(pk=id)
            serializer = QuestionSerializer(question, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(response_json(True, serializer.data, None))
            return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))
        except Question.DoesNotExist as e:
            logging.exception("--------------------------------")
            return Response(response_json(False, None, constants.TEXT_DOES_NOT_EXISTS))
        except Exception as e:
            logging.exception("--------------------------------")
            return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))