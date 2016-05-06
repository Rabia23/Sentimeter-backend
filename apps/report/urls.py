__author__ = 'aamish'

from django.conf.urls import patterns, url
from apps.report import views

urlpatterns = patterns('',
                       url(r'^report$', views.ReportView.as_view()),
                       )
