from django.conf.urls.defaults import patterns, include, url
from django.core.urlresolvers import reverse
from django.contrib import admin
admin.autodiscover()

from landing_page.views import IndexView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name = 'index_view'),
)