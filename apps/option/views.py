from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.option.models import Option
from apps.option.serializers import OptionSerializer
from apps.utils import response_json, get_data_param
from apps import constants


class OptionView(APIView):
    def get(self, request, format=None):
        options = Option.objects.all()
        serializer = OptionSerializer(options, many=True)
        return Response(response_json(True, serializer.data, None))

    @transaction.atomic
    def post(self, request, format=None):
        text = get_data_param(request, 'text', None)

        option = Option.get_if_exists_by_text(text)
        serializer = OptionSerializer(option, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response_json(True, serializer.data, None))
        return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))