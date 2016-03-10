from rest_framework import serializers
from apps.option.models import Option


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('id', 'text', 'score', 'objectId', 'isActive', 'color_code')
