import time
from nose.tools import *
from django.test import TestCase
from nose.plugins.attrib import attr

from aggregator.tests.fixtures.entry import entry
from aggregator.lib.entry_helpers import EntryWrapper

class EntryWrapperTests(TestCase):

	def setUp(self):
		self.entry = entry()
		self.wrapper = EntryWrapper(self.entry)

	def teardown(self):
		pass

	def test_returns_the_correct_set_of_defaults(self):
		required_keys = ['title', 'date_published', 'author']
		defaults = self.wrapper.get_defaults()
		assert_true(all([key in defaults for key in required_keys]))

	def test_date_is_assigned_in_defaults(self):
		date = self.wrapper.get_defaults()['date_published']
		assert_equal(type(date), str)

	def test_date_is_assigned_even_if_not_present_in_entry(self):
		date_less_entry = entry()
		del date_less_entry['updated']
		del date_less_entry['updated_parsed']

		wrapper = EntryWrapper(date_less_entry)
		date = wrapper.get_defaults()['date_published']
		assert_equal(type(date), str)

	def test_date_has_correct_format(self):
		# YYYY-MM-DD HH:MM[:ss[.uuuuuu]]
		date = self.wrapper.get_defaults()['date_published']
		date_as_struct = time.strptime(date, '%Y-%m-%d %H:%M:%S')
		assert_true(type(date_as_struct), time.struct_time)
