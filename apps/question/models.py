from django.db import models
from apps.promotion.models import Promotion
from apps.questionnaire.models import Questionnaire


class Question(models.Model):
    text = models.CharField(max_length=255)
    isActive = models.BooleanField(default=True, db_index=True)
    type = models.IntegerField(db_index=True)
    objectId = models.CharField(max_length=20, db_index=True)
    genreType = models.IntegerField(db_index=True, null=True, blank=True)
    promotion = models.ForeignKey(Promotion, related_name='questions', null=True, blank=True)
    questionnaire = models.ForeignKey(Questionnaire, related_name='questions', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text

    def to_dict(self):
        question = {
            "text": self.text,
            "isActive": self.isActive,
            "type": self.type,
            "objectId": self.objectId,
            "genreType": self.genreType,
            "created_at": self.created_at,
            "options": [option.to_dict() for option in self.options.all()]
        }
        return question

    @staticmethod
    def get_if_exists(object_id):
        question = Question.objects.filter(objectId=object_id).first()
        if question:
            return question
