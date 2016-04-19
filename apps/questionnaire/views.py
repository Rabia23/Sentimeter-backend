from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.branch.models import Branch
from apps.question.models import Question
from apps import constants
from apps.questionnaire.models import Questionnaire
from apps.questionnaire.serializers import QuestionnaireSerializer
from apps.utils import save, response, response_json, get_user_data, get_param, get_data_param
from django.db import transaction
from apps.decorators import my_login_required


class QuestionnaireView(APIView):

    @method_decorator(my_login_required)
    def get(self, request, user, format=None):
        region_id, city_id, branch_id = get_user_data(user)
        if branch_id:
            questionnaires = Questionnaire.objects.filter(branch=branch_id).order_by("-created_at")
        elif region_id:
            questionnaires = Questionnaire.objects.filter(branch__city__region__exact=region_id).order_by("-created_at")
        else:
            questionnaires = Questionnaire.objects.all().order_by("-created_at")
        serializer = QuestionnaireSerializer(questionnaires, many=True)
        return Response(response_json(True, serializer.data, None))

    @transaction.atomic
    def post(self, request, format=None):
        title = get_data_param(request, 'title', None)

        questionnaire = Questionnaire.get_if_exists_by_title(title)
        serializer = QuestionnaireSerializer(questionnaire, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response_json(True, serializer.data, None))
        return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))


class QuestionnaireQuestionsView(APIView):
    def get(self, request, format=None):
        branch_id = get_param(request, 'branch_id', None)
        questionnaire = Questionnaire.objects.filter(isActive=True, branch=branch_id).first()
        data = None
        if questionnaire:
            data = questionnaire.to_dict()
        return Response(response_json(True, data, None))