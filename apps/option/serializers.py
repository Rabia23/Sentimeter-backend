from rest_framework import serializers
from apps.option.models import Option


class OptionSerializer(serializers.ModelSerializer):
    color_code = serializers.CharField(required=False)

    class Meta:
        model = Option
        fields = ('id', 'text', 'score', 'isActive', 'color_code', 'question', 'parent', 'text_urdu')
