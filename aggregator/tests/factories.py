import os
import factory
from aggregator.models import Feed

class FeedFactory(factory.Factory):
	FACTORY_FOR = Feed

	source = os.path.join(os.path.dirname(__file__), 'fixtures/feed.xml')

class InvalidFeedFactory(factory.Factory):
	FACTORY_FOR = Feed

	source = ''
