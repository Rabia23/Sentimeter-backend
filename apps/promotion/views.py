from rest_framework.response import Response
from rest_framework.views import APIView
from apps.promotion.models import Promotion
from apps.promotion.serializers import PromotionSerializer
from apps.question.models import Question
from apps import constants
from apps.utils import save, response, response_json, get_data_param
from django.db import transaction


class PromotionView(APIView):
    def get(self, request, format=None):
        promotions = Promotion.objects.all().order_by("-created_at")
        serializer = PromotionSerializer(promotions, many=True)
        return Response(response_json(True, serializer.data, None))

    @transaction.atomic
    def post(self, request, format=None):
        data = request.data["object"]
        trigger = request.data["triggerName"]

        if trigger == constants.TRIGGER_AFTER_SAVE:
            promotion = Promotion.get_if_exists(data["objectId"])
            serializer = PromotionSerializer(promotion, data=data)
            promotion = save(serializer)

            if "questions" in data:
                question_object_ids = [question_data["objectId"] for question_data in data["questions"]]
                Question.objects.filter(objectId__in=question_object_ids).update(promotion=promotion)

            return response(data)


class PromotionQuestionsView(APIView):
    def get(self, request, format=None):
        promotion = Promotion.objects.filter(isActive=True).first()
        data = None
        if promotion:
            data = promotion.to_dict()
        return Response(response_json(True, data, None))


class PromotionAddView(APIView):

    @transaction.atomic
    def post(self, request, format=None):
        title = get_data_param(request, 'title', None)

        promotion = Promotion.get_if_exists_by_title(title)
        serializer = PromotionSerializer(promotion, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response_json(True, serializer.data, None))
        return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))
