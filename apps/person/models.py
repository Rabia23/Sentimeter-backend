from django.contrib.auth.models import User
from django.db import models
from apps.branch.models import Branch
from apps.branch.serializers import BranchSerializer
from apps.person.enum import UserRolesEnum
from apps.region.models import Region
from apps.region.serializers import RegionSerializer

class UserInfo(models.Model):
    phone_no = models.CharField(max_length=20, null=True, blank=True, db_index=True)
    role = models.IntegerField(default=1, db_index=True)
    gender = models.IntegerField( db_index=True, null=True, blank=True)
    ageGroup = models.IntegerField( db_index=True, null=True, blank=True)
    objectId = models.CharField(max_length=20, db_index=True, null=True, blank=True)
    user = models.ForeignKey(User, related_name='info')
    branch = models.ForeignKey(Branch, related_name='user_info', null=True, blank=True)
    region = models.ForeignKey(Region, related_name='user_info', null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def to_dict(self):
        user_info = {
            "id": self.user.id,
            "username": self.user.username,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "email": self.user.email,
            "phone_no": self.phone_no,
            "role": self.role,
            "branch": BranchSerializer(self.branch).data if self.branch else None,
            "region": RegionSerializer(self.region).data if self.region else None,
            "parent": self.get_parent_dict(),
            "is_active": self.is_active,
        }
        return user_info

    def get_parent_dict(self):
        if self.parent:
            parent = {
                "id": self.parent.user.id,
                "username": self.parent.user.username,
                "first_name": self.parent.user.first_name,
                "last_name": self.parent.user.last_name,
                "email": self.parent.user.email,
                "phone_no": self.parent.phone_no,
                "role": self.parent.role,
                "branch": BranchSerializer(self.parent.branch).data if self.parent.branch else None,
                "region": RegionSerializer(self.parent.region).data if self.parent.region else None,
            }
        else:
            parent = {}
        return parent

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    def has_permission(self):
        if self.role == UserRolesEnum.GRO or self.is_active == False:
            return False
        elif self.role == UserRolesEnum.BRANCH_MANAGER and not self.branch:
            return False
        elif self.role == UserRolesEnum.OPERATIONAL_CONSULTANT and not self.region:
            return False
        return True

    @staticmethod
    def get_person_dict(role, id):
        data = {}
        user_info = UserInfo.objects.filter(user_id=id, role=role).first()
        if user_info:
            data = user_info.to_dict()
        return data

    @staticmethod
    def get_person_dict_by_branch(role, branch_id):
        data = {}
        user_info = UserInfo.objects.filter(branch_id=branch_id, role=role).first()
        if user_info:
            data = user_info.to_dict()
        return data

    @staticmethod
    def get_person_dict_by_region(role, region_id):
        data = {}
        user_info = UserInfo.objects.filter(region_id=region_id, role=role).first()
        if user_info:
            data = user_info.to_dict()
        return data

    @staticmethod
    def get_people_dict(role):
        data = [user_info.to_dict() for user_info in UserInfo.objects.filter(role=role, is_active=True).order_by("-created_at")]
        return data

    @staticmethod
    def get_children_dict(role, parent_role, parent_id):
        data = []
        user_info = UserInfo.objects.filter(user_id=parent_id, role=parent_role).first()
        if user_info:
            data = [user_info.to_dict() for user_info in UserInfo.objects.filter(role=role, parent_id=user_info.id).order_by("-created_at")]
        return data

    @staticmethod
    def get_if_exists(objectId):
        user_info = UserInfo.objects.filter(objectId=objectId).first()
        if user_info:
            return user_info
