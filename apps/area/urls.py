__author__ = 'aamish'

from django.conf.urls import patterns, url
from apps.area import views
from django.views.generic import TemplateView
urlpatterns = patterns('',
                       url(r'^area$', views.AreaView.as_view()),
                       url(r'^index1/$', TemplateView.as_view(template_name="socket_session_test.html")),
                       # url(r'^index2/$', TemplateView.as_view(template_name="socket_session_test2.html")),
                       # url(r'^index3/$', TemplateView.as_view(template_name="tornado_user.html")),
                       )
