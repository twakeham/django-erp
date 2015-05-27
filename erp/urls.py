from django.conf.urls import patterns, include, url
from django.contrib import admin

from core.dynamic.admin import fieldadmin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'erp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),
    url(r'^fields/', include(fieldadmin.urls)),
)
