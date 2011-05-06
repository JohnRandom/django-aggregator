#-*- coding: utf-8 -*-
from datetime import datetime, timedelta

from nose.tools import *
from django.test import TestCase
from nose.plugins.attrib import attr

from django.core.management import call_command as call

import settings
from aggregator.tests.factories import EntryFactory
from aggregator.models import Entry

class CleanEntryTests(TestCase):

	def setUp(self):
		settings.ENTRY_EXPIRATION_DAYS = 7
		delta = timedelta(days = 8)
		publish_date = datetime.now() - delta
		self.entry = EntryFactory(date_published = publish_date)

	def teardown(self):
		pass

	def test_clean_up_should_remove_expired_entries(self):
		assert_equals(Entry.expired.count(), 1)
		call('cleanentries')
		assert_equals(Entry.expired.count(), 0)

	def test_clean_up_should_not_remove_entries_not_yet_expired(self):
		self.entry.date_published = datetime.now()
		self.entry.save()

		assert_equals(Entry.objects.count(), 1)
		call('cleanentries')
		assert_equals(Entry.objects.count(), 1)
