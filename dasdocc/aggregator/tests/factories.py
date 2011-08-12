import os
import factory
from lxml import html
from mock import Mock, mocksignature, MagicMock
from datetime import datetime
from dasdocc.aggregator.models import Feed, Entry
from dasdocc.aggregator.lib.feed_helpers import FeedParser

### Factories

class FeedFactory(factory.Factory):
    FACTORY_FOR = Feed

    source = os.path.join(os.path.dirname(__file__), 'fixtures/feed.xml')

class InvalidFeedFactory(factory.Factory):
    FACTORY_FOR = Feed

    source = ''

class FeedWithEntriesFactory(factory.Factory):
    FACTORY_FOR = Feed

class EntryFactory(factory.Factory):
    FACTORY_FOR = Entry

    title = 'test entry'
    author = 'some guy'
    link = 'some link'
    date_published = datetime.now()
    feed = factory.LazyAttribute(lambda a: FeedFactory())

### Mocks

class PropertyMock(MagicMock):
    def __get__(self, obj, obj_type):
        return self()
    def __set__(self, obj, val):
        self(val)

feed_defaults = {
    'source': 'feed-source',
    'title': 'feed-title',
    'link': 'feed-link',
    'description': 'feed-description',
    'etag': 'feed-etag',
    'date_parsed': 'date',
    'language_code': 'en',
    'language': 'english',
    'content_expiration': 7,
}

class FeedMock(MagicMock):
    source = PropertyMock(return_value='feed-source')
    etag = PropertyMock(return_value='1234')

FeedParserMock = Mock(spec=FeedParser)
FeedParserMock.get_defaults = Mock(return_value=feed_defaults)

class StaticContentMock(MagicMock):
    source = PropertyMock(return_value='http://mocked.source/')

    def __init__(self, selectors=None, *args, **kwargs):
        super(MagicMock, self).__init__(*args, **kwargs)

        if selectors:
            self.selector_set.all = Mock(return_value=selectors)

class SelectorMock(MagicMock):
    css_selector = PropertyMock(return_value='div#content')

static_content_html = '<html><head></head><body><div id="content"><a href="/test">a link</a></div></body></html>'
def static_content_parsed():
     return html.fromstring(static_content_html)

def static_content_with_childs(amount=10, tag='div', class_='test',
    value='test'):

    start = '<html><head></head><body>'
    end = '</body></html>'

    content = []
    content_template = '<%s class="%s">%s</%s>'

    for i in range(amount):
        content.append(content_template % (tag, class_, value, tag))

    static_content_html = start + ''.join(content) + end
    return html.fromstring(static_content_html)
