from django.conf.urls.defaults import patterns, include, url
from aggregator.views import PlaygroundView
from aggregator.models import StaticContent, Feed

urlpatterns = patterns('aggregator.views',
    url(r'^playground/$', PlaygroundView.as_view(), name = 'playground_view'),
	url(r'^update/$', 'update_content', {'model': [StaticContent, Feed], 'next': '/playground/'}, name = 'update_view'),
)
