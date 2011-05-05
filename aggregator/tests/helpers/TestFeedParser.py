import nose.tools as nt
from django.test import TestCase
from nose.plugins.attrib import attr

from aggregator.tests.factories import FeedFactory, InvalidFeedFactory
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

	def test_feed_parser_should_wrap_all_entries(self):
		entries = self.parser.get_entries()
		nt.assert_true(all([isinstance(e, EntryWrapper) for e in entries]))

	def test_feed_parser_should_not_parse_on_init(self):
		nt.assert_equal(self.parser.feed, None)

	def test_feed_parser_defaults_should_containt_required_keys(self):
		required_keys = ['title', 'link', 'description', 'etag', 'language_code']
		defaults = self.parser.get_defaults()
		nt.assert_true(all([k in defaults for k in required_keys]))

	def test_feed_parser_should_not_raise_errors_on_valid_feeds(self):
		self.parser.get_entries()
		nt.assert_true(not self.parser.error['raised'])

	def test_feed_parser_should_mark_feed_as_valid(self):
		nt.assert_true(self.parser.is_valid())

class FeedParserWithInvalidFeedTests(TestCase):

	def setUp(self):
		self.parser = FeedParser(InvalidFeedFactory.build())

	def teardown(self):
		pass

	def test_feed_parser_should_set_error_on_invalid_feeds(self):
		self.parser.get_defaults()
		nt.assert_true(self.parser.error['raised'])

	def test_feed_parser_should_return_empty_entries_array(self):
		nt.assert_equal(self.parser.get_entries(), [])

	def test_feed_parser_should_mark_feed_as_invalid(self):
		nt.assert_true(not self.parser.is_valid())

	def test_feed_parser_assigns_no_defaults(self):
		defaults = self.parser.get_defaults()
		nt.assert_true(all([val is None for key, val in defaults.iteritems()]))
