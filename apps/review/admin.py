# from api.views import DataView
from .models import Feedback, Question, Option,HomeDeliveryUsers,MessageDelayTime
from django.conf.urls import patterns
from django.contrib import admin
from django.http import HttpResponse
#
#
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('comment','type',)

#
#
# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ('text',)
#
#
# class OptionAdmin(admin.ModelAdmin):
#     list_display = ('text',)
#
#
# def get_admin_urls(urls):
#     def get_urls():
#         my_urls = patterns('',
#             (r'^data_view/$', admin.site.admin_view(DataView.as_view()))
#         )
#         return my_urls + urls
#     return get_urls
#

class HomeDeliveryUsersAdmin(admin.ModelAdmin):
    list_display = ('name',)
class MessageDelayTimeAdmin(admin.ModelAdmin):
    list_display = ('minutes',)

admin.site.register(HomeDeliveryUsers, HomeDeliveryUsersAdmin)
admin.site.register(MessageDelayTime, MessageDelayTimeAdmin)

admin.site.register(Feedback, FeedbackAdmin)
# admin.site.register(Question, QuestionAdmin)
# admin.site.register(Option, OptionAdmin)
#
# admin_urls = get_admin_urls(admin.site.get_urls())
# admin.site.get_urls = admin_urls