import feedparser
from landing_page.models import Feed

def register_feed(url, parse_instantly = False):
	if parse_instantly:
		parser = FeedParser(url)
		try: f, new = Feed.objects.get_or_create(**parser.get_defaults())
		except Exception as e: raise e
	else:
		f, new = Feed.objects.get_or_create(link = url)
		f.save()

	return f

class DecoratorError(Exception):
	pass

def parse_feed(method):

	def wrapper(*args, **kwargs):
		inst = args[0]
		if not isinstance(inst, FeedParser): raise DecoratorError("parse_feed can only be used with FeedParser.")
		if inst.feed is None: inst.feed = feedparser.parse(inst.url)
		return method(*args, **kwargs)

	return wrapper

class FeedParser(object):

	def __init__(self, url):
		self.url = url
		self.feed = None

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
