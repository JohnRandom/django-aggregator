from django.db import models
from django.db.models.signals import post_save
from aggregator.lib.feed_helpers import FeedParser
from aggregator.receiver import feed_created

class Feed(models.Model):

	source = models.URLField("Source", max_length = 255)
	title = models.CharField("Title", max_length = 255, null = True, blank = True)
	link = models.URLField("Link", max_length = 255, null = True, blank = True)
	description = models.CharField("Description", max_length = 255, null = True, blank = True)
	etag = models.CharField("ETag", max_length = 255, null = True, blank = True)
	date_parsed = models.DateTimeField("Last visited", auto_now = True)

	def update(self):
		if not self.id: raise self.NotUpdatetableError("Feed instances must be saved, before they can be updated.")

		parser = FeedParser(self)

		# update feed
		if parser.get_feed().status == 304: return
		self.__dict__.update(**parser.get_defaults())
		self.save()

		# update entries
		[self.entry_set.create(**entry.get_defaults()) for entry in parser.get_entries()]

	def __unicode__(self):
		return unicode(self.title or self.source)

	@models.permalink
	def get_absolute_url(self):
		raise NotImplementedError()

	class NotUpdatetableError(Exception):
		pass

class Entry(models.Model):

	title = models.CharField("Title", max_length = 255)
	author = models.CharField("Author", max_length = 255)
	date_published = models.DateTimeField()
	feed = models.ForeignKey(Feed)

	class Meta:
		unique_together = ('title', 'author', 'date_published', 'feed')
		ordering = ('-date_published',)

	def __unicode__(self):
		return unicode(self.title)

post_save.connect(feed_created, sender = Feed)
