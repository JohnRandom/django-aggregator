from django.conf.urls.defaults import patterns, include, url
from aggregator.views import PlaygroundView

urlpatterns = patterns('',
    url(r'^playground/$', PlaygroundView.as_view()),
)
