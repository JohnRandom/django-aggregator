from django.conf.urls.defaults import patterns, include, url
from django.core.urlresolvers import reverse
from django.contrib import admin
admin.autodiscover()

from landing_page.views import IndexView

urlpatterns = patterns('',
	url(r'^$', IndexView.as_view(), name = 'index_view'),
	url(r'^admin/', include(admin.site.urls)),
	url(r'aggregator/', include('aggregator.urls')),
	url(r'^accounts/login/$', 'django.contrib.auth.views.login', name = 'login_view'),
	url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name = 'logout_view'),
)
