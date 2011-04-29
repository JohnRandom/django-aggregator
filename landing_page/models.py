from django.db import models
from django.db.models.signals import post_save
from lib.feed_helpers import FeedParser
from landing_page.receiver import feed_created

class Feed(models.Model):

	source = models.URLField("Source", max_length = 255)
	title = models.CharField("Title", max_length = 255, null = True, blank = True)
	link = models.URLField("Link", max_length = 255, null = True, blank = True)
	description = models.CharField("Description", max_length = 255, null = True, blank = True)
	etag = models.CharField("ETag", max_length = 255, null = True, blank = True)
	date_parsed = models.DateTimeField("Last visited", auto_now = True)

	def update(self, and_save = True):
		parser = FeedParser(self)
		self.__dict__.update(**parser.get_defaults())
		if and_save:
			if not self.id: raise self.NotUpdatetableError("Feed instances must be saved, before they can be updated.")
			self.save()

	def __unicode__(self):
		return unicode(self.title or self.source)

	@models.permalink
	def get_absolute_url(self):
		raise NotImplementedError()

	class NotUpdatetableError(Exception):
		pass


def register_feed(source, parse_instantly = False):
	f, new = Feed.get_or_create(source = url)
	parser = FeedParser(source)

	if parse_instantly:
		try:
			f = update_feed(f, **parser.get_defaults())
			f.save()
		except Exception as e:
			raise e

	return f

post_save.connect(feed_created, sender = Feed)
