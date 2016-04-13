__author__ = 'aamish'

from django.conf.urls import patterns, url
from apps.option import views

urlpatterns = patterns('',
                       url(r'^option$', views.OptionView.as_view()),
                       )
