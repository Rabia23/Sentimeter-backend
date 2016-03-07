__author__ = 'aamish'

from django.conf.urls import patterns, url
from apps.review import views

urlpatterns = patterns('',
                       url(r'^feedback/$', views.FeedbackView.as_view()),
                       )
