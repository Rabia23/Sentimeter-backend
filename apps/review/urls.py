__author__ = 'aamish'

from django.conf.urls import patterns, url
from apps.review import views

urlpatterns = patterns('',
                       url(r'^feedback$', views.FeedbackView.as_view()),
                       url(r'^batch_feedback$', views.FeedbackBatchView.as_view()),
                       url(r'^allfeedback$', views.AllFeedbackView.as_view()),
                       url(r'^meesagefeedback$', views.MessageFeedBackView),
                       url(r'^meesagefeedbackrec$', views.MessageFeedBackViewRec),
                       url(r'^plivo$', views.plivo_message_send),
                       url(r'^twilliosms$', views.twillio_message_send),
                       url(r'^sms/$', views.sms),
                       url(r'^abc/$', views.ahah),
                       url(r'^messagebird$', views.messagebird1),
                       url(r'^clickatell$', views.clickatell),
                       # url(r'^sms/', views.sms_plain),
                       # url(r'^ring/$', views.ring),

                       )
