from django.db import models
from apps.branch.models import Branch


class Questionnaire(models.Model):
    title = models.CharField(max_length=255)
    isActive = models.BooleanField(default=True, db_index=True)
    branch = models.ManyToManyField(Branch, related_name='questionnaire')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.title

    def to_dict(self):
        questionnaire = {
            "title": self.title,
            "isActive": self.isActive,
            "created_at": self.created_at,
            "questions": [question.to_dict() for question in self.questions.all()]
        }
        return questionnaire

    @staticmethod
    def get_if_exists(object_id):
        questionnaire = Questionnaire.objects.filter(objectId=object_id).first()
        if questionnaire:
            return questionnaire

    @staticmethod
    def get_if_exists_by_title(title):
        questionnaire = Questionnaire.objects.filter(title=title).first()
        if questionnaire:
            return questionnaire
