from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.conf import settings

from core.dynamic.admin import fieldadmin

from apps.checklist.views import show_checklist


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'erp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),
    url(r'^fields/', include(fieldadmin.urls)),
    url(r'^checklist/([a-zA-Z0-9]+)/$', show_checklist)
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
   )