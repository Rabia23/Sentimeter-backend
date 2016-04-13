__author__ = 'aamish'

from django.conf.urls import patterns, url
from apps.questionnaire import views

urlpatterns = patterns('',
                       url(r'^questionnaire$', views.QuestionnaireView.as_view()),
                       url(r'^questionnaire_question$', views.QuestionnaireQuestionsView.as_view()),
                       url(r'^questionnaire_add$', views.QuestionnaireAddView.as_view()),
                       )
