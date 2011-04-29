import feedparser
from landing_page.models import Feed

ALLOWED_STATUS_CODES = [200, 301, 302]

def update_feed(feed, **kwargs):
	if not isinstance(feed, Feed): raise TypeError("Can only update instances of Feed, got %s" % feed.__class__.__name__)
	feed.__dict__.update(**kwargs)
	return feed

def register_feed(url, parse_instantly = False):
	f, new = Feed.get_or_create(link = url)
	parser = FeedParser(url)

	if parse_instantly:
		try:
			f = update_feed(f, **parser.get_defaults())
			f.save()
		except Exception as e:
			raise e

	return f

class DecoratorError(Exception):
	pass

class FeedParsingError(Exception):
	pass

def parse_feed(method):

	def wrapper(*args, **kwargs):
		inst = args[0]
		if not isinstance(inst, FeedParser): raise DecoratorError("parse_feed can only be used with FeedParser.")
		if inst.feed is None:
			inst.feed = feed = feedparser.parse(inst.url)
		return method(*args, **kwargs)

	return wrapper

class FeedParser(object):

	def __init__(self, url):
		self.url = url
		self.feed = None

		try: self.model = Feed.objects.get(link = url)
		except Feed.DoesNotExist: self.model = None

	@parse_feed
	def _map_content(self):
		feed = self.feed

		return {
			'title': feed.feed.title,
			'link': feed.feed.link,
			'description': feed.feed.title,
			'etag': feed.etag,
		}

	@parse_feed
	def get_defaults(self):
		feed = self.feed
		return self._map_content()

	@parse_feed
	def get_entries(self):
		return self.feed.entries

	@parse_feed
	def get_feed(self):
		return self.feed

	def is_valid(self):

	@parse_feed
	def is_valid(feed):
		if hasattr(self.feed, 'status') and not self.feed.status in ALLOWED_STATUS_CODES:
			return False
		elif self.feed.feed == {}:
			return False
		return True
