from rest_framework import serializers


class FeedbackCommentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    objectId = serializers.CharField()
    comment = serializers.CharField()
    branch = serializers.CharField()
    city = serializers.CharField()
    region = serializers.CharField()
    segment = serializers.CharField()
    shift = serializers.CharField()
    user_name = serializers.CharField()
    user_phone = serializers.CharField()
    is_negative = serializers.BooleanField()
    action_taken = serializers.IntegerField()
    email = serializers.CharField()


class ObjectSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

