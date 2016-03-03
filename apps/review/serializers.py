from rest_framework import serializers
from apps.review.models import Feedback, FeedbackOption
from drf_haystack.serializers import HaystackSerializer

from apps.review.models import Feedback
from apps.review.search_indexes import FeedbackIndex


class FeedbackSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    comment = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    objectId = serializers.CharField()
    gro_name = serializers.CharField(required=False)
    action_taken = serializers.CharField(required=False)

    class Meta:
        model = Feedback
        

class FeedbackOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackOption
        fields = ('id', 'feedback', 'option')


class FeedbackSearchSerializer(HaystackSerializer):

    class Meta:
        # The `index_classes` attribute is a list of which search indexes
        # we want to include in the search.
        index_classes = [FeedbackIndex]

        # The `fields` contains all the fields we want to include.
        # NOTE: Make sure you don't confuse these with model attributes. These
        # fields belong to the search index!
        fields = [
            "text", "comment",
        ]
