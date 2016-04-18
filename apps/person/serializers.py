from django.contrib.auth.models import User
from rest_framework import serializers
from apps.person.models import UserInfo

__author__ = 'aamish'


class UserInfoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    phone_no = serializers.CharField(required=False)

    class Meta:
        model = UserInfo
        fields = ('id', 'phone_no', 'user', 'gender', 'ageGroup')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'password', 'email')


