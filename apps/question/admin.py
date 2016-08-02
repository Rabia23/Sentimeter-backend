from django.contrib import admin
from .models import Question,Questionnaire
# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    pass
class QuestionnaireAdmin(admin.ModelAdmin):
    pass

admin.site.register(Question, QuestionAdmin)
admin.site.register(Questionnaire, QuestionnaireAdmin)