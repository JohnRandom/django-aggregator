import feedparser
from lib.entry_helpers import EntryWrapper

ALLOWED_STATUS_CODES = [200, 301, 302, 304]

class DecoratorError(Exception):
	pass

class FeedParsingError(Exception):
	pass

def parse_feed(method):

	def wrapper(*args, **kwargs):
		inst = args[0]
		if not isinstance(inst, FeedParser): raise DecoratorError("parse_feed can only be used with FeedParser.")
		if inst.feed is None:
			inst.feed = feed = feedparser.parse(inst.source, etag = inst.model.etag)
			if not inst.is_valid():
				print inst.feed.status
				raise FeedParsingError()
		return method(*args, **kwargs)

	return wrapper

class FeedParser(object):

	def __init__(self, feed_instance):
		self.source = feed_instance.source
		self.model = feed_instance
		self.feed = None

	@parse_feed
	def _map_content(self):
		feed = self.feed

		return {
			'title': feed.feed.title if hasattr(feed.feed, 'title') else None,
			'link': feed.feed.link if hasattr(feed.feed, 'link') else None,
			'description': feed.feed.description if hasattr(feed.feed, 'description') else None,
			'etag': feed.etag if hasattr(feed, 'etag') else None,
		}

	@parse_feed
	def get_defaults(self):
		return self._map_content()

	@parse_feed
	def get_entries(self):
		return map(lambda x: EntryWrapper(x, self.model), self.feed.entries)

	@parse_feed
	def raw_entries(self):
		return self.feed.entries

	@parse_feed
	def get_feed(self):
		return self.feed

	@parse_feed
	def is_valid(self):
		if hasattr(self.feed, 'status') and not self.feed.status in ALLOWED_STATUS_CODES:
			return False
		return True
