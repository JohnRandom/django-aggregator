from django.test import TestCase
import nose.tools as nt
from nose.plugins.attrib import attr

from aggregator.tests.factories import FeedFactory
from aggregator.lib.feed_helpers import FeedParser

class FeedParserTests(TestCase):

	def setUp(self):
		self.feed = FeedFactory.build()

	def teardown(self):
		pass

	def test_feedparser_should_parse_before_get_defaults(self):
		parser = FeedParser(self.feed)
		parser.get_defaults()
		nt.assert_equal(parser.feed.feed.title, 'c-base logbuch')
