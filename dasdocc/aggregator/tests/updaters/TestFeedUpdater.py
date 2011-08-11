#-*- coding: utf-8 -*-
from datetime import datetime, timedelta

from nose.tools import *
from django.test import TestCase
from nose.plugins.attrib import attr

from dasdocc.aggregator.lib.updaters.feed_updater import _FeedUpdater, truncate
from dasdocc.aggregator.tests.factories import FeedFactory
from dasdocc.aggregator.models import Entry

from mock import patch

class FeedUpdaterTests(TestCase):

	def setUp(self):
		self.updater = _FeedUpdater

	def teardown(self):
		pass

	def test_expired_entries_should_not_get_saved(self):
		parser = self.updater(FeedFactory(content_expiration = 0))
		parser.run()
		assert_equals(Entry.objects.count(), 0)

class TruncateTests(TestCase):

	def setUp(self):
		self.FIELDS = {
			'field1': 10,
			'field2': 10,
			'field3': 25,
		}
		self.test_data = {
			'field1': '____5___10___15',
			'field2': '____5___10___15___20',
			'field3': '____5___10___15',
		}

	def teardown(self):
		pass

	def test_truncation_of_fields_works_properly(self):
		with patch.dict('dasdocc.aggregator.lib.updaters.feed_updater.FEED_FIELDS', self.FIELDS):
			result = truncate(self.test_data)

			assert_equals(len(result['field1']), 10)
			assert_equals(len(result['field2']), 10)
			assert_equals(len(result['field3']), 15)

	def test_proper_use_of_truncator(self):
		with patch.dict('dasdocc.aggregator.lib.updaters.feed_updater.FEED_FIELDS', self.FIELDS):
			result = truncate(self.test_data)
			assert_true(result['field1'].endswith('...'))

	def test_truncation_does_not_happen_on_unspecified_fields(self):
		with patch.dict('dasdocc.aggregator.lib.updaters.feed_updater.FEED_FIELDS', self.FIELDS):
			test_data = self.test_data
			test_data['unspecified_field'] = 'a'
			result = truncate(self.test_data)

			assert_equals(result['unspecified_field'], 'a')

	def test_truncator_should_handle_NoneType_content(self):
		with patch.dict('dasdocc.aggregator.lib.updaters.feed_updater.FEED_FIELDS', self.FIELDS):
			test_data = self.test_data
			test_data['field1'] = None
			result = truncate(self.test_data)

			assert_equals(result['field1'], None)