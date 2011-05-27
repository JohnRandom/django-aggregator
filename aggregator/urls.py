from django.conf.urls.defaults import patterns, include, url
from aggregator.views import PlaygroundView, update_content
from aggregator.models import StaticContent, Feed

urlpatterns = patterns('',
    url(r'^playground/$', PlaygroundView.as_view()),
	url(r'^update/$', update_content, {'model': [StaticContent, Feed], 'next': '/playground/'}),
)
