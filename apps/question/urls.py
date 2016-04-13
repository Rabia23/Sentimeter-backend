__author__ = 'aamish'

from django.conf.urls import patterns, url
from apps.question import views

urlpatterns = patterns('',
                       url(r'^question$', views.QuestionView.as_view()),
                       url(r'^question_add$', views.QuestionAddView.as_view()),
                       )
