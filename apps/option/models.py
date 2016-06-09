from django.db import models
from apps.question.models import Question


class Option(models.Model):
    text = models.CharField(max_length=255)
    text_urdu = models.CharField(max_length=255)
    score = models.IntegerField(default=0, db_index=True)
    question = models.ForeignKey(Question, related_name='options', null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    isActive = models.BooleanField(default=True, db_index=True)
    color_code = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    sequence = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.text

    def to_dict(self):
        option = {
            "id": self.id,
            "text": self.text,
            "text_urdu": self.text_urdu,
            "isActive": self.isActive,
            "score": self.score,
            "color_code": self.color_code,
            "created_at": self.created_at,
            "sequence": self.sequence,
            "children": [child.to_dict() for child in self.children.filter(isActive=True)]
        }
        return option

    def to_object_dict(self):
        option = {
            "id": self.id,
            "text": self.text,
            "color_code": self.color_code
        }
        return option

    @staticmethod
    def get_if_exists(object_id):
        option = Option.objects.filter(objectId=object_id).first()
        if option:
            return option

    @staticmethod
    def get_if_exists_by_text(text):
        option = Option.objects.filter(text=text).first()
        if option:
            return option

    def is_parent(self):
        return self.children.count() > 0
