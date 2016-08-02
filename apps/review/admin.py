# from api.views import DataView
from .models import Feedback, FeedbackOption
from django.conf.urls import patterns
from django.contrib import admin
from django.http import HttpResponse

#
class FeedbackAdmin(admin.ModelAdmin):
    pass
#
#
# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ('text',)
#
#
class FeedbackOptionAdmin(admin.ModelAdmin):
    list_display = ["feedback","option"]
    pass
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
admin.site.register(Feedback, FeedbackAdmin)
# admin.site.register(Question, QuestionAdmin)
admin.site.register(FeedbackOption, FeedbackOptionAdmin)
#
# admin_urls = get_admin_urls(admin.site.get_urls())
# admin.site.get_urls = admin_urls