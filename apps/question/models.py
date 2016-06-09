from django.db import models
from apps import constants
from apps.promotion.models import Promotion
from apps.questionnaire.models import Questionnaire
from django_boto.s3.storage import S3Storage

s3 = S3Storage()


class Question(models.Model):
    text = models.CharField(max_length=255)
    text_urdu = models.CharField(max_length=255)
    isActive = models.BooleanField(default=True, db_index=True)
    type = models.IntegerField(db_index=True)
    genreType = models.IntegerField(db_index=True, null=True, blank=True)
    promotion = models.ForeignKey(Promotion, related_name='questions', null=True, blank=True)
    questionnaire = models.ForeignKey(Questionnaire, related_name='questions', null=True, blank=True)
    image = models.ImageField(storage=s3, blank=True, null=True, upload_to='questions')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    sequence = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.text

    def to_dict(self):
        if self.type and self.type == constants.TYPE_1:
            options = [option.to_dict() for option in self.options.filter(isActive=True).order_by("-score")]
        else:
            options = [option.to_dict() for option in self.options.filter(isActive=True).order_by("created_at")]
        question = {
            "id": self.id,
            "text": self.text,
            "text_urdu": self.text_urdu,
            "isActive": self.isActive,
            "type": self.type,
            "sequence": self.sequence,
            "genreType": self.genreType,
            "image": self.image.url if self.image else None,
            "created_at": self.created_at,
            "options": options,
        }
        return question

    @staticmethod
    def get_if_exists(object_id):
        question = Question.objects.filter(objectId=object_id).first()
        if question:
            return question

    @staticmethod
    def get_if_exists_by_text(text):
        question = Question.objects.filter(text=text).first()
        if question:
            return question
