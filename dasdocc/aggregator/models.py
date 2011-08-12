from datetime import datetime, timedelta

from django.db import models
from django.db.models.signals import post_save

from dasdocc.aggregator.lib.updaters.feed_updater import FeedUpdater
from dasdocc.aggregator.lib.updaters.static_content_updater import StaticContentUpdater
from dasdocc.aggregator.managers import UntrashedFeedManager, TrashedFeedManager

from taggit.managers import TaggableManager


class SourceCategory(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode(self.name)


class Feed(models.Model):

    source = models.CharField("Source", max_length=255)
    title = models.CharField("Title", max_length=255, null=True, blank=True)
    link = models.URLField("Link", max_length=255, null=True, blank=True)
    description = models.CharField("Description", max_length=255, null=True,
        blank=True)
    etag = models.CharField("ETag", max_length=255, null=True, blank=True)
    date_parsed = models.DateTimeField("Last visited", auto_now=True)
    language = models.CharField("Language", max_length=100, blank=True,
        null=True)
    language_code = models.CharField("Language Code", max_length=50, blank=True,
        null=True)
    valid = models.BooleanField(default=True)
    trashed_at = models.DateTimeField("Trashed", blank=True, null=True)
    content_expiration = models.SmallIntegerField("Content expiration",
        default=7)
    category = models.ForeignKey(SourceCategory, blank=True, null=True)

    objects = UntrashedFeedManager()
    trashed = TrashedFeedManager()
    updater = FeedUpdater()

    def __unicode__(self):
        return unicode(self.title or self.source)

    def is_ok(self):
        return not self.parsingerror_set.count() > 0
    is_ok.boolean = True

    def get_expired_entries(self):
        delta = timedelta(days=self.content_expiration)
        treshold = datetime.now() - delta

        return self.entry_set.filter(date_published__lte=treshold)

    @models.permalink
    def get_absolute_url(self):
        raise NotImplementedError()

    def save(self, and_update=False, *args, **kwargs):
        saved = super(Feed, self).save(*args, **kwargs)
        if and_update: self.updater.run()
        return saved

    class NotUpdatetableError(Exception):
        pass


class ParsingError(models.Model):

    feed = models.ForeignKey(Feed)
    error_message = models.CharField('Error message', max_length=255)
    date_raised = models.DateTimeField('occured at', auto_now_add=True)

    class Meta:
        ordering = ('-date_raised',)

    def __unicode__(self):
        return unicode('"%s" on feed: %s' % (self.error_message, self.feed))


class Entry(models.Model):

    title = models.CharField("Title", max_length=255)
    author = models.CharField("Author", max_length=255)
    link = models.CharField("Link", max_length=255)
    date_published = models.DateTimeField()
    feed = models.ForeignKey(Feed)

    tags = TaggableManager(blank=True)
    objects = models.Manager()

    class Meta:
        ordering = ('-date_published',)

    def __unicode__(self):
        return unicode(self.title)


class StaticContent(models.Model):

    name = models.CharField(max_length=255, unique=True)
    source = models.URLField('Source', max_length=255)
    date_parsed = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(SourceCategory, blank=True, null=True)

    updater = StaticContentUpdater()

    def is_ok(self):
        return not self.staticcontenterror_set.count() > 0
    is_ok.boolean = True

    def log_error(self, e):
        StaticContentError.objects.create(
            source = self,
            error = e.__class__.__name__,
            message = e.message,
        )

    def get_expired_entries(self):
        return self.selector_set.none()

    def __unicode__(self):
        return unicode(self.name or self.source)


class Selector(models.Model):

    parent = models.ForeignKey(StaticContent)
    css_selector = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)
    bound_content = models.TextField(blank=True, null=True)
    max_amount_of_childs = models.SmallIntegerField(blank=True, null=True)

    def __unicode__(self):
        return unicode(self.css_selector)


class StaticContentError(models.Model):

    source = models.ForeignKey(StaticContent)
    error = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    date_raised = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_raised',)

    def __unicode__(self):
        return unicode("'%s' on source: %s" % (self.error, self.source))
