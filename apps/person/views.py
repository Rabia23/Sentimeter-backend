from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView
from apps import constants
from apps.branch.models import Branch
from apps.decorators import my_login_required
from apps.parse import ParseHelper
from apps.person.enum import UserRolesEnum
from apps.person.models import UserInfo
from apps.region.models import Region
from apps.utils import get_data_param, get_param, get_default_param, response_json, create_user
from django.db import IntegrityError
from django.utils.decorators import method_decorator


class UserView(APIView):

    @method_decorator(my_login_required)
    def get(self, request, user, format=None):
        role = get_param(request, 'role', None)
        id = get_param(request, 'id', None)
        director_id = get_param(request, 'director_id', None)
        assistant_director_id = get_param(request, 'assistant_director_id', None)
        operational_manager_id = get_param(request, 'operational_manager_id', None)
        operational_consultant_id = get_param(request, 'operational_consultant_id', None)
        branch_manager_id = get_param(request, 'branch_manager_id', None)

        if id:
            data = UserInfo.get_person_dict(int(role), id)
        elif director_id:
            data = UserInfo.get_children_dict(UserRolesEnum.ASSISTANT_DIRECTOR, UserRolesEnum.DIRECTOR, director_id)
        elif assistant_director_id:
            data = UserInfo.get_children_dict(UserRolesEnum.OPERATIONAL_MANAGER, UserRolesEnum.ASSISTANT_DIRECTOR, assistant_director_id)
        elif operational_manager_id:
            data = UserInfo.get_children_dict(UserRolesEnum.OPERATIONAL_CONSULTANT, UserRolesEnum.OPERATIONAL_MANAGER, operational_manager_id)
        elif operational_consultant_id:
            data = UserInfo.get_children_dict(UserRolesEnum.BRANCH_MANAGER, UserRolesEnum.OPERATIONAL_CONSULTANT, operational_consultant_id)
        elif branch_manager_id:
            data = UserInfo.get_children_dict(UserRolesEnum.GRO, UserRolesEnum.BRANCH_MANAGER, branch_manager_id)
        else:
            data = UserInfo.get_people_dict(int(role))

        return Response(response_json(True, data, None))

    @method_decorator(my_login_required)
    @transaction.atomic()
    def post(self, request, user, format=None):
        try:
            role = get_data_param(request, 'role', None)
            username = get_data_param(request, 'username', None)
            first_name = get_data_param(request, 'first_name', None)
            last_name = get_data_param(request, 'last_name', None)
            password = get_data_param(request, 'password', None)
            email = get_data_param(request, 'email', None)
            phone_no = get_data_param(request, 'phone_no', None)
            branch_id = get_data_param(request, 'branch_id', None)
            region_id = get_data_param(request, 'region_id', None)
            parent_id = get_data_param(request, 'parent_id', None)

            if role:
                branch = Branch.objects.get(pk=branch_id) if branch_id else None
                parent_user = User.objects.get(pk=parent_id) if parent_id else None
                parent = parent_user.info.first() if parent_user else None
                region = Region.objects.get(pk=region_id) if region_id else None

                if branch and parent:
                    if role == UserRolesEnum.GRO:
                        user = create_user(username, first_name, last_name, email, password)
                        user_info = UserInfo.objects.create(user=user, phone_no=phone_no, role=UserRolesEnum.GRO,
                                                            branch=branch, parent=parent)
                        parse_helper = ParseHelper()
                        parse_helper.item_add(user_info, password)
                        return Response(response_json(True, user_info.to_dict(), None))
                    elif role == UserRolesEnum.BRANCH_MANAGER:
                        if not branch.is_associated():
                            user = create_user(username, first_name, last_name, email, password)
                            user_info = UserInfo.objects.create(user=user, phone_no=phone_no, role=UserRolesEnum.BRANCH_MANAGER,
                                                        branch=branch, parent=parent)
                            return Response(response_json(True, user_info.to_dict(), None))
                        else:
                            return Response(response_json(False, None, "Branch already Associated"))
                elif region and parent:
                    if role == UserRolesEnum.OPERATIONAL_CONSULTANT:
                        if not region.is_associated():
                            user = create_user(username, first_name, last_name, email, password)
                            user_info = UserInfo.objects.create(user=user, phone_no=phone_no, role=UserRolesEnum.OPERATIONAL_CONSULTANT,
                                                        region=region, parent=parent)
                            return Response(response_json(True, user_info.to_dict(), None))
                        else:
                            return Response(response_json(False, None, "Region already Associated"))
                elif parent:
                    if role == UserRolesEnum.OPERATIONAL_MANAGER:
                        user = create_user(username, first_name, last_name, email, password)
                        user_info = UserInfo.objects.create(user=user, phone_no=phone_no,
                                            role=UserRolesEnum.OPERATIONAL_MANAGER, parent=parent)
                        return Response(response_json(True, user_info.to_dict(), None))
                    elif role == UserRolesEnum.ASSISTANT_DIRECTOR:
                        user = create_user(username, first_name, last_name, email, password)
                        user_info = UserInfo.objects.create(user=user, phone_no=phone_no,
                                            role=UserRolesEnum.ASSISTANT_DIRECTOR, parent=parent)
                        return Response(response_json(True, user_info.to_dict(), None))
                else:
                    if role == UserRolesEnum.DIRECTOR:
                        user = create_user(username, first_name, last_name, email, password)
                        user_info = UserInfo.objects.create(user=user, phone_no=phone_no, role=UserRolesEnum.DIRECTOR)
                        return Response(response_json(True, user_info.to_dict(), None))

            return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))
        except IntegrityError as e:
            return Response(response_json(False, None, "Username" + constants.TEXT_ALREADY_EXISTS))

    @method_decorator(my_login_required)
    @transaction.atomic()
    def put(self, request, user, format=None):
        try:
            id = get_data_param(request, 'id', None)
            new_password = get_data_param(request, 'new_password', None)
            email = get_data_param(request, 'email', None)
            phone_no = get_data_param(request, 'phone_no', None)
            first_name = get_data_param(request, 'first_name', None)
            last_name = get_data_param(request, 'last_name', None)
            branch_id = get_data_param(request, 'branch_id', None)
            region_id = get_data_param(request, 'region_id', None)

            branch = Branch.objects.get(pk=branch_id) if branch_id else None
            region = Region.objects.get(pk=region_id) if region_id else None

            if branch and branch.is_associated():
                return Response(response_json(False, None, "Branch is already Associated"))
            elif region and region.is_associated():
                return Response(response_json(False, None, "Region is already Associated"))

            user = User.objects.get(pk=id)
            if user:
                user.email = email if email else user.email
                if new_password:
                    user.set_password(new_password)
                user.first_name = first_name if first_name else user.first_name
                user.last_name = last_name if last_name else user.last_name
                user.save()

            user_info = user.info.first()
            if user_info:
                user_info.branch_id = branch.id if branch else user_info.branch_id
                user_info.region_id = region.id if region else user_info.region_id
                user_info.phone_no = phone_no if phone_no else user_info.phone_no
                user_info.save()
            return Response(response_json(True, user_info.to_dict(), None))

        except User.DoesNotExist as e:
            return Response(response_json(False, None, constants.TEXT_DOES_NOT_EXISTS))
        except Branch.DoesNotExist as e:
            return Response(response_json(False, None, constants.TEXT_DOES_NOT_EXISTS))
        except Region.DoesNotExist as e:
            return Response(response_json(False, None, constants.TEXT_DOES_NOT_EXISTS))

    @method_decorator(my_login_required)
    @transaction.atomic()
    def delete(self, request, user, format=None):
        try:
            id = get_default_param(request, 'id', None)

            user = User.objects.get(pk=id)
            if user:
                user_info = user.info.first()
                if user_info:
                    if user_info.is_active:
                        user_info.is_active = False
                    else:
                        user_info.is_active = True
                    user_info.save()
                    return Response(response_json(True, user_info.to_dict(), None))

            return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))
        except User.DoesNotExist as e:
            return Response(response_json(False, None, constants.TEXT_DOES_NOT_EXISTS))


class DisassociateBranchRegionView(APIView):

    @method_decorator(my_login_required)
    def get(self, request, user, format=None):
        try:
            id = get_param(request, 'id', None)

            user = User.objects.get(pk=id)
            if user:
                user_info = user.info.first()
                if user_info:
                    if user_info.role == UserRolesEnum.BRANCH_MANAGER or user_info.role == UserRolesEnum.GRO:
                        user_info.branch_id = None
                        user_info.save()
                    elif user_info.role == UserRolesEnum.OPERATIONAL_CONSULTANT:
                        user_info.region_id = None
                        user_info.save()
                    return Response(response_json(True, user_info.to_dict(), None))

            return Response(response_json(False, None, constants.TEXT_OPERATION_UNSUCCESSFUL))
        except User.DoesNotExist as e:
            return Response(response_json(False, None, constants.TEXT_DOES_NOT_EXISTS))
