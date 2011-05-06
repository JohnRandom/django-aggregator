import datetime

from django.db import models
from django.db.models.signals import post_save

from aggregator.lib.feed_helpers import FeedParser
from aggregator.receiver import feed_created
from aggregator.managers import UntrashedFeedManager, TrashedFeedManager

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
	trashed_at = models.DateTimeField(blank = True, null = True)

	objects = UntrashedFeedManager()
	trashed = TrashedFeedManager()

	def update(self):
		if not self.id: raise self.NotUpdatetableError("Feed instances must be saved, before they can be updated.")

		parser = FeedParser(self)
		defaults = parser.get_defaults()

		# update feed
		if parser.feed.get('status', False) == 304: return
		self.__dict__.update(**defaults)
		self._map_language()
		self.save()

		# update entries
		for entry in parser.get_entries():
			e, new = self.entry_set.get_or_create(**entry.get_defaults())
			e.tags.set(*entry.get_tags())

		# create parsing errors if necessary
		if parser.error['raised']:
			self.parsingerror_set.create(error_message = parser.error['message'][:255])

		# validate and trash if necessary
		self.valid = parser.is_valid()
		if not self.valid and self.trashed_at is None: self.trashed_at = datetime.datetime.now()
		self.save()
		return self.valid

	def _map_language(self):

		language_map = {
			'en': 'english',
			'de': 'german',
		}

		self.language = language_map.get(self.language_code, 'unknown')

	def __unicode__(self):
		return unicode(self.title or self.source)

	@models.permalink
	def get_absolute_url(self):
		raise NotImplementedError()

	def save(self, and_update = False, *args, **kwargs):
		saved = super(Feed, self).save(*args, **kwargs)
		if and_update: self.update()
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

	class Meta:
		ordering = ('-date_published',)

	def __unicode__(self):
		return unicode(self.title)
