#-*- coding: utf-8 -*-
from datetime import datetime, timedelta

from nose.tools import *
from django.test import TestCase
from nose.plugins.attrib import attr

from aggregator.lib.updaters.feed_updater import _FeedUpdater
from aggregator.tests.factories import FeedFactory
from aggregator.models import Entry

class FeedUpdaterTests(TestCase):

	def setUp(self):
		self.updater = _FeedUpdater

	def teardown(self):
		pass

	@attr('wip')
	def test_expired_entries_should_not_get_saved(self):
		parser = self.updater(FeedFactory(content_expiration = 0))
		parser.run()
		assert_equals(Entry.objects.count(), 0)

