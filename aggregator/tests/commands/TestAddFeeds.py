from nose.tools import *
from nose.plugins.attrib import attr
from django.test import TestCase
from django.core.management import call_command as call

from aggregator.tests.factories import FeedFactory, InvalidFeedFactory
from aggregator.models import Feed

class AddValidFeedsTests(TestCase):

	def setUp(self):
		self.feed = FeedFactory.build()

	def teardown(self):
		pass

	def test_adding_valid_feeds_works(self):
		call('addfeeds', self.feed.source)
		assert_equals(Feed.objects.count(), 1)

	def test_adding_feeds_should_not_update_by_default(self):
		call('addfeeds', self.feed.source)
		assert_equals(Feed.objects.get().title, None)

class AddInvalidFeedsTests(TestCase):

	def setUp(self):
		self.feed = InvalidFeedFactory.build()

	def teardown(self):
		pass

	def test_adding_invalid_feeds_works(self):
		call('addfeeds', self.feed.source)
		assert_equals(Feed.objects.count(), 1)

	def test_adding_feeds_should_not_update_by_default(self):
		call('addfeeds', self.feed.source)
		assert_equals(Feed.objects.get().title, None)
