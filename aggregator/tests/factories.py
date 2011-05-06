import os
import factory
from datetime import datetime
from aggregator.models import Feed, Entry

class FeedFactory(factory.Factory):
	FACTORY_FOR = Feed

	source = os.path.join(os.path.dirname(__file__), 'fixtures/feed.xml')

class InvalidFeedFactory(factory.Factory):
	FACTORY_FOR = Feed

	source = ''

class EntryFactory(factory.Factory):
	FACTORY_FOR = Entry

	title = 'test entry'
	author = 'some guy'
	link = 'some link'
	date_published = datetime.now()
	feed = factory.LazyAttribute(lambda a: FeedFactory())

