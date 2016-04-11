from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps import constants
from apps.area.serializers import AreaSerializer
from apps.utils import get_data_param, response_json
from apps.area.models import Area
from django.db import transaction


class AreaView(APIView):
    def get(self, request, format=None):
        areas = Area.objects.all()
        serializer = AreaSerializer(areas, many=True)
        return Response(response_json(True, serializer.data, None))

    @transaction.atomic
    def post(self, request, format=None):
        name = get_data_param(request, 'name', None)
        area = Area.get_if_exists(name)
        serializer = AreaSerializer(area, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response_json(True, serializer.data, None))
        return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))