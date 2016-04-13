__author__ = 'aamish'

from django.conf.urls import patterns, url
from apps.person import views

urlpatterns = patterns('',
                       url(r'^user$', views.UserView.as_view()),
                       url(r'^disassociate$', views.DisassociateBranchRegionView.as_view()),
                       url(r'^branch_gro$', views.BranchGroView.as_view()),
                       )
