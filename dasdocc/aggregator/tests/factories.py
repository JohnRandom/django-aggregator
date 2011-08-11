import os
import factory
from lxml import html
from mock import Mock, mocksignature
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

class PropertyMock(Mock):
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

class FeedMock(Mock):
	source = PropertyMock(return_value = 'feed-source')
	etag = PropertyMock(return_value = '1234')

FeedParserMock = Mock(spec = FeedParser)
FeedParserMock.get_defaults = Mock(return_value = feed_defaults)

class StaticContentMock(Mock):
	source = PropertyMock(return_value = 'http://mocked.source/')

class SelectorMock(Mock):
	css_selector = PropertyMock(return_value = 'div#content')

static_content_html = '<html><head></head><body><div id="content"><a href="/test">a link</a></div></body></html>'
static_content_parsed = html.fromstring(static_content_html)