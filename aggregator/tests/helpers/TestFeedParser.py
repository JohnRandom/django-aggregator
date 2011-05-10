from nose.tools import *
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
		assert_equal(self.parser.feed.feed.title, 'c-base logbuch')

	def test_feed_parser_should_wrap_all_entries(self):
		entries = self.parser.get_entries()
		assert_true(all([isinstance(e, EntryWrapper) for e in entries]))

	def test_feed_parser_should_not_parse_on_init(self):
		assert_equal(self.parser.feed, None)

	def test_feed_parser_defaults_should_containt_required_keys_and_values(self):
		defaults = self.parser.get_defaults()
		assert_equals(defaults['description'], u'culture communication carbonite')
		assert_equals(defaults['link'], u'http://logbuch.c-base.org')
		assert_equals(defaults['title'], u'c-base logbuch')
		assert_equals(defaults['language_code'], u'en')
		assert_equals(defaults['language'], u'english')
		assert_true('etag' in defaults.keys())

	def test_feed_parser_should_not_raise_errors_on_valid_feeds(self):
		self.parser.get_entries()
		assert_true(not self.parser.error['raised'])

class FeedParserWithInvalidFeedTests(TestCase):

	def setUp(self):
		self.parser = FeedParser(InvalidFeedFactory.build())

	def teardown(self):
		pass

	def test_feed_parser_should_set_error_on_invalid_feeds(self):
		self.parser.get_defaults()
		assert_true(self.parser.error['raised'])

	def test_feed_parser_should_return_empty_entries_array(self):
		assert_equal(self.parser.get_entries(), [])

	def test_feed_parser_should_return_correct_validation_status(self):
		assert_true(not self.parser.is_valid())

	def test_feed_parser_assigns_no_defaults(self):
		defaults = self.parser.get_defaults()
		assert_true(all([val is None for key, val in defaults.iteritems()]))
