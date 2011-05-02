from django.test import TestCase
import nose.tools as nt
from nose.plugins.attrib import attr

from aggregator.tests.factories import FeedFactory
from aggregator.lib.feed_helpers import FeedParser
from aggregator.lib.entry_helpers import EntryWrapper

class FeedParserTests(TestCase):

	def setUp(self):
		self.parser = FeedParser(FeedFactory.build())

	def teardown(self):
		pass

	def test_feedparser_should_parse_before_get_defaults(self):
		self.parser.get_defaults()
		nt.assert_equal(self.parser.feed.feed.title, 'c-base logbuch')

	def test_feed_parser_should_parse_before_get_entries(self):
		self.parser.get_entries()
		nt.assert_equal(self.parser.feed.feed.title, 'c-base logbuch')

	def test_feed_parser_should_wrap_all_entries(self):
		entries = self.parser.get_entries()
		nt.assert_true(all([isinstance(e, EntryWrapper) for e in entries]))

	def test_feed_parser_should_not_parse_on_init(self):
		nt.assert_equal(self.parser.feed, None)

	def test_feed_parser_defaults_should_containt_required_keys(self):
		required_keys = ['title', 'link', 'description', 'etag']
		defaults = self.parser.get_defaults()
		nt.assert_true(all([k in defaults for k in required_keys]))

	def test_feed_parser_should_not_raise_errors_on_valid_feeds(self):
		self.parser.get_entries()
		nt.assert_true(not self.parser.error['raised'])
