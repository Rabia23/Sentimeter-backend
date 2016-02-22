__author__ = 'aamish'

from django.conf.urls import patterns, url
from apps.questionnaire import views

urlpatterns = patterns('',
                       url(r'^questionnaire/$', views.QuestionnaireView.as_view()),
                       )
