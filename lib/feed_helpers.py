import feedparser

class FeedParser(object):

	def __init__(self, url):
		self.url = url
		self.feed = None

	def _parse(self):
		if self.feed is None:
			self.feed = feed = feedparser.parse(self.url)
		else:
			feed = self.feed

		return feed

	def _map_content(self):
		feed = self.feed

		return {
			'title': feed.feed.title,
			'link': feed.feed.link,
			'description': feed.feed.title,
			'etag': feed.etag,
		}

	def get_defaults(self):
		feed = self._parse()
		return self._map_content()

	def get_entries(self):
		return self.feed.entries




#>>> d.feed.title
#u'Sample Feed'
#>>> d.feed.link
#u'http://example.org/'
#>>> d.feed.description
#u'For documentation <em>only</em>'
#>>> d.feed.date
#u'Sat, 07 Sep 2002 0:00:01 GMT'
#>>> d.feed.date_parsed
#(2002, 9, 7, 0, 0, 1, 5, 250, 0)
