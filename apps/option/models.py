from django.db import models
from apps.question.models import Question


class Option(models.Model):
    text = models.CharField(max_length=255)
    objectId = models.CharField(max_length=20, db_index=True)
    score = models.IntegerField(default=0, db_index=True)
    question = models.ForeignKey(Question, related_name='options', null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text

    @staticmethod
    def get_if_exists(object_id):
        option = Option.objects.filter(objectId=object_id).first()
        if option:
            return option

    def is_parent(self):
        return self.children.count() > 0