from django.conf.urls.defaults import patterns, include, url
from dasdocc.aggregator.views import PlaygroundView
from dasdocc.aggregator.models import StaticContent, Feed

urlpatterns = patterns('dasdocc.aggregator.views',
    url(r'^playground/$', PlaygroundView.as_view(), name = 'playground_view'),
	url(r'^update/$', 'update_content', {'model': [StaticContent, Feed]}, name = 'update_view'),
)
