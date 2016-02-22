from django.conf.urls import include, url, patterns
from django.contrib import admin
from lively import settings
from apps.area import urls as area_urls
from apps.region import urls as region_urls
from apps.city import urls as city_urls
from apps.branch import urls as branch_urls
from apps.promotion import urls as promotion_urls
from apps.question import urls as question_urls
from apps.option import urls as option_urls
from apps.review import urls as review_urls
from apps.person import urls as person_urls
from apps.questionnaire import urls as questionnaire_urls
from apps import urls as api_urls
from apps.dashboard import urls as dashboard_urls


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(area_urls)),
    url(r'^api/', include(region_urls)),
    url(r'^api/', include(city_urls)),
    url(r'^api/', include(branch_urls)),
    url(r'^api/', include(promotion_urls)),
    url(r'^api/', include(question_urls)),
    url(r'^api/', include(option_urls)),
    url(r'^api/', include(review_urls)),
    url(r'^api/', include(person_urls)),
    url(r'^api/', include(questionnaire_urls)),
    url(r'^api/', include(api_urls)),
    url(r'^dashboard/', include(dashboard_urls)),
    url(r'^swagger/', include('rest_framework_swagger.urls')),
]

if not settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )