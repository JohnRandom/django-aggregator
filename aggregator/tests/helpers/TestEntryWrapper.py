#-*- coding: utf-8 -*-
import time
from datetime import datetime
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
		required_keys = ['title', 'date_published', 'author', 'link']
		defaults = self.wrapper.get_defaults()
		assert_true(all([key in defaults for key in required_keys]))

	@attr('wip')
	def test_returns_the_correct_values_for_defaults(self):
		d = self.wrapper.get_defaults()
		assert_equals(d['title'], u'Ubuntu 11.04 \u201eNatty Narwhal\u201c Releaseparty 21.05.2011')
		assert_equals(d['date_published'], datetime(2011, 04, 29, 20, 11, 43))
		assert_equals(d['author'], u'macro')
		assert_equals(d['link'], u'http://logbuch.c-base.org/archives/1170')

	@attr('wip')
	def test_date_is_assigned_even_if_not_present_in_entry(self):
		date_less_entry = entry()
		del date_less_entry['updated']
		del date_less_entry['updated_parsed']

		wrapper = EntryWrapper(date_less_entry)
		defaults = wrapper.get_defaults()
		assert_true(defaults.get('date_published', False))

	@attr('wip')
	def test_date_as_datetime(self):
		date = self.wrapper.get_defaults()['date_published']
		assert_true(isinstance(date, datetime))

	def test_wrapper_should_parse_tags(self):
		tags = self.wrapper.get_tags()
		assert_equals(tags.sort(), ['bordleben', 'cience', 'com'].sort())

	def test_wrapper_should_return_empty_list_if_not_tags_are_available(self):
		del self.wrapper.entry['tags']
		tags = self.wrapper.get_tags()
		assert_equals(tags, [])
