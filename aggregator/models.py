from datetime import datetime

from django.db import models
from django.db.models.signals import post_save

from aggregator.lib.updaters.feed_updater import FeedUpdater
from aggregator.managers import UntrashedFeedManager, TrashedFeedManager, ExpiredEntriesManager

from taggit.managers import TaggableManager

class Feed(models.Model):

	source = models.CharField("Source", max_length = 255)
	title = models.CharField("Title", max_length = 255, null = True, blank = True)
	link = models.URLField("Link", max_length = 255, null = True, blank = True)
	description = models.CharField("Description", max_length = 255, null = True, blank = True)
	etag = models.CharField("ETag", max_length = 255, null = True, blank = True)
	date_parsed = models.DateTimeField("Last visited", auto_now = True)
	language = models.CharField("Language", max_length = 100, blank = True, null = True)
	language_code = models.CharField("Language Code", max_length = 50, blank = True, null = True)
	valid = models.BooleanField(default = True)
	trashed_at = models.DateTimeField("Trashed", blank = True, null = True)
	content_expiration = models.SmallIntegerField("Content expiration", default = 7)

	objects = UntrashedFeedManager()
	trashed = TrashedFeedManager()
	updater = FeedUpdater()

	def __unicode__(self):
		return unicode(self.title or self.source)

	@models.permalink
	def get_absolute_url(self):
		raise NotImplementedError()

	def save(self, and_update = False, *args, **kwargs):
		saved = super(Feed, self).save(*args, **kwargs)
		if and_update: self.updater.run()
		return saved

	class NotUpdatetableError(Exception):
		pass

class ParsingError(models.Model):

	feed = models.ForeignKey(Feed)
	error_message = models.CharField('Error message', max_length = 255)
	date_raised = models.DateTimeField('occured at', auto_now_add = True)

	class Meta:
		ordering = ('-date_raised',)

	def __unicode__(self):
		return unicode('"%s" on feed: %s' % (self.error_message, self.feed))

class Entry(models.Model):

	title = models.CharField("Title", max_length = 255)
	author = models.CharField("Author", max_length = 255)
	link = models.CharField("Link", max_length = 255)
	date_published = models.DateTimeField()
	feed = models.ForeignKey(Feed)

	tags = TaggableManager()
	objects = models.Manager()
	expired = ExpiredEntriesManager()

	class Meta:
		ordering = ('-date_published',)

	def __unicode__(self):
		return unicode(self.title)
