import feedparser
from aggregator.lib.entry_helpers import EntryWrapper

ALLOWED_STATUS_CODES = [200, 301, 302, 304]

class DecoratorError(Exception):
	pass

class FeedParsingError(Exception):
	pass

def parse_feed(method):
	'''
	A simple feed cache decorator, that ensures each method on FeedParser using the feed
	content has parsed the feed already. If the feed was parsed once, it's results
	will be saved and reused each time the feed is accessed.
	'''

	def wrapper(*args, **kwargs):
		inst = args[0]
		if not isinstance(inst, FeedParser): raise DecoratorError("parse_feed can only be used with FeedParser.")
		if inst.feed is None:
			inst.feed = feed = feedparser.parse(inst.source, etag = inst.model.etag)
			if not inst.is_valid():
				raise FeedParsingError()
		return method(*args, **kwargs)

	return wrapper

class FeedParser(object):
	'''
	FeedParser is a thin wrapper around the object returned by feedparser.parse(). It's
	job is to provide an easy interface to access the necessary attributes for Feed model
	creation and entry parsing.
	Use it to safely access the feed content.
	'''

	def __init__(self, feed_instance):
		self.source = feed_instance.source
		self.model = feed_instance
		self.feed = None

	@parse_feed
	def _map_content(self):
		feed = self.feed

		return {
			'title': feed.feed.get('title', None),
			'link': feed.feed.get('link', None),
			'description': feed.feed.get('description', None),
			'etag': feed.get('etag', None),
		}

	@parse_feed
	def get_defaults(self):
		'''
		Provides the fields necessary for Feed creation as dictionary.
		'''
		return self._map_content()

	@parse_feed
	def get_entries(self):
		'''
		Returns the entry list with each element wrapped in an EntryWrapper.
		'''
		return map(lambda x: EntryWrapper(x, self.model), self.feed.entries)

	@parse_feed
	def raw_entries(self):
		return self.feed.entries

	@parse_feed
	def get_feed(self):
		return self.feed

	@parse_feed
	def is_valid(self):
		if hasattr(self.feed, 'status') and self.feed.status in ALLOWED_STATUS_CODES:
			return True
		return False
