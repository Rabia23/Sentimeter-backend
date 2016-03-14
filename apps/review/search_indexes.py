__author__ = 'aamish'

from haystack import indexes
from apps.review.models import Feedback


class FeedbackIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    id = indexes.IntegerField(model_attr="id")
    action_taken = indexes.IntegerField(model_attr="action_taken")
    comment = indexes.CharField(model_attr="comment", null=True, default=None)
    created_at = indexes.DateTimeField(model_attr="created_at")

    branch = indexes.IntegerField()
    region = indexes.IntegerField()

    def get_updated_field(self):
        return "updated"

    def prepare_branch(self, obj):
        return obj.branch.id

    def prepare_region(self, obj):
        return obj.branch.city.region.id

    def get_model(self):
        return Feedback

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
