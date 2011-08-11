from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.core.urlresolvers import reverse
from django.contrib import admin

from django.conf.urls.static import static

admin.autodiscover()

from landing_page.views import IndexView

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
	url(r'aggregator/', include('dasdocc.aggregator.urls')),
	url(r'^accounts/login/$', 'django.contrib.auth.views.login', name = 'login_view'),
	url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name = 'logout_view'),
)

if settings.DEBUG:
    # urlpatterns += staticfiles_urlpatterns()
    # urlpatterns += patterns('',
    #     (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    #     (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT }),
    # )
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += patterns('',
	url(r'', include('landing_page.urls')),
)
