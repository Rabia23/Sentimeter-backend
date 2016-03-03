__author__ = 'aamish'

from haystack import indexes
from apps.review.models import Feedback


class FeedbackIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    comment = indexes.CharField(model_attr="comment", null=True, default="")

    autocomplete = indexes.EdgeNgramField()

    @staticmethod
    def prepare_autocomplete(obj):
        return " ".join((
            str(obj.comment)
        ))

    def get_model(self):
        return Feedback

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
