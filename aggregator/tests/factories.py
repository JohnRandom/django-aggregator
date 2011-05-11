import os
import factory
from mock import Mock, mocksignature
from datetime import datetime
from aggregator.models import Feed, Entry
from aggregator.lib.feed_helpers import FeedParser

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
