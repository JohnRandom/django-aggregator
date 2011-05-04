from nose.tools import *
from django.test import TestCase
from nose.plugins.attrib import attr

from aggregator.tests.factories import FeedFactory, InvalidFeedFactory
from aggregator.models import Feed, Entry, ParsingError

class testif(object):

	def __init__(self, condition):
		self.condition = condition

	def __call__(self, func):
		def wrapper(*args, **kwargs):
			return func(*args, **kwargs) if self.condition else True
		return wrapper

class TestFeed(TestCase):

	def setUp(self):
		self.feed = FeedFactory.build()

	def teardown(self):
		pass

	def test_feed_update_has_to_be_specified(self):
		self.feed.save()
		assert_false(Entry.objects.count())

		self.feed.update()
		assert_equals(Entry.objects.count(), 10)

	def test_feed_update_on_save_is_configurable(self):
		self.feed.save(and_update = True)
		assert_equals(Entry.objects.count(), 10)

	def test_update_should_not_create_duplicate_entries(self):
		self.feed.save(and_update = True)
		self.feed.update()
		assert_equals(Entry.objects.count(), 10)

	@raises(Feed.NotUpdatetableError)
	def test_feed_update_should_raise_error_on_unsaved_instances(self):
		feed = FeedFactory.build(source = 'some-feed-url')
		self.feed.update()

	def test_feed_update_should_set_values_on_instance(self):
		self.feed.save(and_update = True)
		assert_equals(self.feed.description, u'culture communication carbonite')
		assert_equals(self.feed.link, u'http://logbuch.c-base.org')
		assert_equals(self.feed.title, u'c-base logbuch')

	def test_feed_update_should_log_parsing_errors(self):
		feed = InvalidFeedFactory()
		feed_valid = feed.update()
		assert_equals(ParsingError.objects.count(), 1)

	def test_feed_update_should_return_valid_status(self):
		feed = InvalidFeedFactory()
		feed_valid = feed.update()
		assert_false(feed_valid)
