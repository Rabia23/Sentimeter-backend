from django.db import models


class Promotion(models.Model):
    title = models.CharField(max_length=255)
    isActive = models.BooleanField(default=True, db_index=True)
    toggle_colors = models.BooleanField(default=True, db_index=True)
    color_selected = models.CharField(max_length=10, blank=True, null=True)
    color_unselected = models.CharField(max_length=10, blank=True, null=True)
    objectId = models.CharField(max_length=20, db_index=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.title

    def to_dict(self):
        promotion = {
            "title": self.title,
            "isActive": self.isActive,
            "objectId": self.objectId,
            "created_at": self.created_at,
            "questions": [question.to_dict() for question in self.questions.all()]
        }
        return promotion

    @staticmethod
    def get_if_exists(object_id):
        promotion = Promotion.objects.filter(objectId=object_id).first()
        if promotion:
            return promotion

    @staticmethod
    def get_if_exists_by_title(title):
        promotion = Promotion.objects.filter(title=title).first()
        if promotion:
            return promotion
