#-*- coding: utf-8 -*-
from datetime import datetime, timedelta

from nose.tools import *
from django.test import TestCase
from nose.plugins.attrib import attr

from aggregator.tests.factories import FeedFactory, InvalidFeedFactory
from aggregator.models import Feed, Entry, ParsingError

from taggit.models import Tag

class testif(object):

	def __init__(self, condition):
		self.condition = condition

	def __call__(self, func):
		def wrapper(*args, **kwargs):
			return func(*args, **kwargs) if self.condition else True
		return wrapper

class TestValidFeed(TestCase):

	def setUp(self):
		self.feed = FeedFactory.build()

	def teardown(self):
		pass

	def test_feed_update_has_to_be_specified(self):
		self.feed.save()
		assert_false(Entry.objects.count())

		self.feed.updater.run()
		assert_equals(Entry.objects.count(), 10)

	def test_feed_update_on_save_is_configurable(self):
		self.feed.save(and_update = True)
		assert_equals(Entry.objects.count(), 10)

	def test_update_should_not_create_duplicate_entries(self):
		self.feed.save(and_update = True)
		self.feed.updater.run()
		assert_equals(Entry.objects.count(), 10)

	@raises(ValueError)
	def test_feed_update_should_raise_error_on_unsaved_instances(self):
		feed = FeedFactory.build(source = 'some-feed-url')
		feed.updater.run()

	def test_feed_update_should_set_values_on_instance(self):
		self.feed.save(and_update = True)
		assert_equals(self.feed.description, u'culture communication carbonite')
		assert_equals(self.feed.link, u'http://logbuch.c-base.org')
		assert_equals(self.feed.title, u'c-base logbuch')
		assert_equals(self.feed.language_code, u'en')
		assert_equals(self.feed.language, u'english')

	def test_feed_update_should_log_parsing_errors(self):
		feed = InvalidFeedFactory()
		feed_valid = feed.updater.run()
		assert_equals(ParsingError.objects.count(), 1)

	def test_feed_update_should_return_false_if_invalid(self):
		feed = InvalidFeedFactory()
		feed_valid = feed.updater.run()
		assert_false(feed_valid)

	def test_feed_update_should_return_true_if_valid(self):
		feed = FeedFactory()
		feed_valid = feed.updater.run()
		assert_true(feed_valid)

	def test_update_should_generate_tags_for_entries(self):
		assert_equals(Tag.objects.count(), 0)
		self.feed.save(and_update = True)
		assert_equals(Tag.objects.count(), 16)

	def test_valid_feeds_should_not_be_trashed(self):
		self.feed.save(and_update = True)
		assert_equals(self.feed.trashed_at, None)
		assert_true(self.feed in Feed.objects.all())
		assert_false(self.feed in Feed.trashed.all())

	def test_trashed_feeds_never_update(self):
		self.feed.trashed_at = datetime.now()
		self.feed.save()

		assert_false(self.feed.updater.run())

class TestInvalidFeed(TestCase):

	def setUp(self):
		self.feed = InvalidFeedFactory.build()
		delta = timedelta(hours = 2)
		self.time_trashed = datetime.now() - delta
		self.already_trashed_feed = FeedFactory.build(trashed_at = self.time_trashed)

	def test_feed_parser_should_trash_invalid_feeds(self):
		self.feed.save(and_update = True)
		assert_true(self.feed.trashed_at)
		assert_true(self.feed in Feed.trashed.all())
		assert_false(self.feed in Feed.objects.all())

	def test_invalid_feeds_should_be_trashed_more_than_once(self):
		self.already_trashed_feed.save(and_update = True)
		assert_equals(self.already_trashed_feed.trashed_at, self.time_trashed)

	def test_trashed_feeds_should_not_be_updated(self):
		assert_equals(self.already_trashed_feed.title, None)
		self.already_trashed_feed.save(and_update = True)
		assert_equals(self.already_trashed_feed.title, None)

class CustomManagerTests(TestCase):

	def setUp(self):
		delta = timedelta(hours = 2)
		time_trashed = datetime.now() - delta
		self.valid_feed = FeedFactory()
		self.invalid_feed = InvalidFeedFactory(trashed_at = time_trashed)

	def tearfown(self):
		pass

	def test_objects_just_returns_not_trashed_feeds(self):
		assert_equals(Feed.objects.get(), self.valid_feed)

	def test_trashed_just_returns_not_trashed_feeds(self):
		assert_equals(Feed.trashed.get(), self.invalid_feed)
