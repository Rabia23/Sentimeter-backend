from rest_framework.response import Response
from rest_framework.views import APIView
from apps.branch.models import Branch
from apps.question.models import Question
from apps import constants
from apps.questionnaire.models import Questionnaire
from apps.questionnaire.serializers import QuestionnaireSerializer
from apps.utils import save, response, response_json
from django.db import transaction


class QuestionnaireView(APIView):
    def get(self, request, format=None):
        questionnaires = Questionnaire.objects.all().order_by("-created_at")
        serializer = QuestionnaireSerializer(questionnaires, many=True)
        return Response(response_json(True, serializer.data, None))

    @transaction.atomic
    def post(self, request, format=None):
        data = request.data["object"]
        trigger = request.data["triggerName"]

        if trigger == constants.TRIGGER_AFTER_SAVE:
            questionnaire = Questionnaire.get_if_exists(data["objectId"])
            serializer = QuestionnaireSerializer(questionnaire, data=data)
            questionnaire = save(serializer)

            branch = Branch.objects.get(pk=data["branch"])
            questionnaire.branch.add(branch)
            questionnaire.save()

            if "questions" in data:
                question_object_ids = [question_data["objectId"] for question_data in data["questions"]]
                Question.objects.filter(objectId__in=question_object_ids).update(questionnaire=questionnaire)

            return response(data)