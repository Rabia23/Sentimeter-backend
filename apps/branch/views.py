from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView
from apps import constants
from apps.branch.models import Branch
from apps.branch.serializers import BranchSerializer
from apps.utils import get_data_param, response_json, get_user_data
from django.db import transaction
from apps.decorators import my_login_required


class BranchView(APIView):
    def get(self, request, format=None):
        region_id = request.query_params.get('region', None)
        city_id = request.query_params.get('city', None)
        if region_id:
            branches = Branch.objects.filter(city__region__exact=region_id)
        elif city_id:
            branches = Branch.objects.filter(city__exact=city_id)
        else:
            branches = Branch.objects.all()
        serializer = BranchSerializer(branches, many=True)
        return Response(response_json(True, serializer.data, None))

    @transaction.atomic
    def post(self, request, format=None):
        name = get_data_param(request, 'name', None)
        city_id = get_data_param(request, 'city_id', None)

        request.data["city"] = city_id
        branch = Branch.get_if_exists(name)
        serializer = BranchSerializer(branch, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response_json(True, serializer.data, None))
        return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))


class SpecificBranchView(APIView):

    @method_decorator(my_login_required)
    def get(self, request, user, format=None):
        region_id, city_id, branch_id = get_user_data(user)

        if branch_id:
            branches = Branch.objects.filter(id=branch_id)
        elif region_id:
            branches = Branch.objects.filter(city__region__exact=region_id)
        else:
            branches = Branch.objects.all()
        serializer = BranchSerializer(branches, many=True)
        return Response(response_json(True, serializer.data, None))