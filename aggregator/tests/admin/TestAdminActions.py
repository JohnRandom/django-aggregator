#-*- coding: utf-8 -*-
from datetime import datetime, timedelta

from nose.tools import *
from django.test import TestCase
from nose.plugins.attrib import attr

from aggregator.tests.factories import FeedFactory, InvalidFeedFactory
from aggregator.models import Feed, Entry
from aggregator.admin import update_feeds

class AdminActionTests(TestCase):

	def setUp(self):
		self.feed = FeedFactory.build()

	def teardown(self):
		pass

	def test_update_feed_action_updates_feeds(self):
		self.feed.save()
		assert_equals(Entry.objects.count(), 0)

		update_feeds('aModelManager', 'aRequest', [self.feed])
		assert_equals(Entry.objects.count(), 10)
