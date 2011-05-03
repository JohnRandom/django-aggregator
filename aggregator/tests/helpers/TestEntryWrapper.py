import nose.tools as nt
from django.test import TestCase
from nose.plugins.attrib import attr

from aggregator.tests.factories import FeedFactory, InvalidFeedFactory
from aggregator.tests.fixtures.entry import entry
from aggregator.lib.feed_helpers import FeedParser
from aggregator.lib.entry_helpers import EntryWrapper

class EntryWrapperTests(TestCase):

	def setUp(self):
		self.entry = entry()

	def teardown(self):
		pass

	def test_returns_the_correct_set_of_defaults(self):
		required_keys = ['title', 'date_published', 'author']
		ew = EntryWrapper(self.entry)
		defaults = ew.get_defaults()
		nt.assert_true(all([key in defaults for key in required_keys]))
