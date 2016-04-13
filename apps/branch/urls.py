__author__ = 'aamish'

from django.conf.urls import patterns, url
from apps.branch import views

urlpatterns = patterns('',
                       url(r'^branch$', views.BranchView.as_view()),
                       )
