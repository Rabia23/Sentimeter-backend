from django.db import models
from django_boto.s3.storage import S3Storage

s3 = S3Storage()


class Promotion(models.Model):
    title = models.CharField(max_length=255)
    isActive = models.BooleanField(default=True, db_index=True)
    toggle_colors = models.BooleanField(default=True, db_index=True)
    color_selected = models.CharField(max_length=10, blank=True, null=True)
    color_unselected = models.CharField(max_length=10, blank=True, null=True)
    objectId = models.CharField(max_length=20, db_index=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    banner_image = models.ImageField(storage=s3, blank=True, null=True, upload_to='promotions')
    background_image = models.ImageField(storage=s3, blank=True, null=True, upload_to='promotions')

    def __str__(self):
        return self.title

    def to_dict(self):
        promotion = {
            "title": self.title,
            "isActive": self.isActive,
            "objectId": self.objectId,
            "toggle_colors": self.toggle_colors,
            "color_selected": self.color_selected,
            "color_unselected": self.color_unselected,
            "background_image": self.background_image.url if self.background_image else None,
            "banner_image": self.banner_image.url if self.banner_image else None,
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
