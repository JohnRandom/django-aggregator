from datetime import datetime, timedelta

from nose.tools import *
from nose.plugins.attrib import attr
from django.test import TestCase
from django.core.management import call_command as call

from dasdocc.aggregator.tests.factories import FeedFactory, InvalidFeedFactory
from dasdocc.aggregator.models import Feed

class TrashFeedsTests(TestCase):

	def setUp(self):
		two_hours = timedelta(hours = 2)
		time_invalidated = datetime.now() - two_hours
		self.feed = InvalidFeedFactory(trashed_at = time_invalidated)

	def teardown(self):
		pass

	def test_trashing_invalid_feeds_works(self):
		assert_equals(Feed.trashed.count(), 1)
		call('trashfeeds')
		assert_equals(Feed.trashed.count(), 0)

	def test_valid_feeds_never_gets_trashed(self):
		feed = FeedFactory(trashed_at = None)
		assert_equals(Feed.objects.count(), 1)
		call('trashfeeds')
		assert_equals(Feed.objects.count(), 1)

	def test_invalid_feeds_only_get_deleted_when_they_are_marked_as_trash(self):
		assert_equals(Feed.trashed.count(), 1)
		self.feed.trashed_at = None
		self.feed.save()
		call('trashfeeds')

		self.feed.trashed_at = datetime.now()
		self.feed.save()
		assert_equals(Feed.trashed.count(), 1)
