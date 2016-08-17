__author__ = 'aamish'

from django.conf.urls import patterns, url
from apps.review import views

urlpatterns = patterns('',
                       url(r'^feedback$', views.FeedbackView.as_view()),
                       url(r'^batch_feedback$', views.FeedbackBatchView.as_view()),
                       url(r'^home_delivery$', views.HomeDeliveryUsersView.as_view()),
                       )
