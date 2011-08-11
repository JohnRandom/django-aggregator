from nose.tools import *
from nose.plugins.attrib import attr
from django.test import TestCase
from django.core.management import call_command as call

from dasdocc.aggregator.tests.factories import FeedFactory, InvalidFeedFactory
from dasdocc.aggregator.models import Feed

class UpdateValidFeedsTests(TestCase):

	def setUp(self):
		self.feed = FeedFactory()

	def teardown(self):
		pass

	def test_updating_valid_feeds_works(self):
		assert_equals(Feed.objects.get().title, None)
		call('updatefeeds')
		assert_equals(Feed.objects.get().title, u'c-base logbuch')

	def test_updating_does_not_delete_valid_tests(self):
		assert_equals(Feed.objects.count(), 1)
		call('updatefeeds')
		assert_equals(Feed.objects.count(), 1)

