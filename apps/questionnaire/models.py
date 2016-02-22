from django.db import models
from apps.branch.models import Branch


class Questionnaire(models.Model):
    title = models.CharField(max_length=255)
    isActive = models.BooleanField(default=True, db_index=True)
    branch = models.ManyToManyField(Branch, related_name='questionnaire')
    objectId = models.CharField(max_length=20, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.title

    @staticmethod
    def get_if_exists(object_id):
        questionnaire = Questionnaire.objects.filter(objectId=object_id).first()
        if questionnaire:
            return questionnaire
