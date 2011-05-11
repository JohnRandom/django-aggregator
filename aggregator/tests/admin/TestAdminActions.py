#-*- coding: utf-8 -*-
from datetime import datetime, timedelta

from nose.tools import *
from django.test import TestCase
from nose.plugins.attrib import attr

from aggregator.tests.factories import FeedFactory, InvalidFeedFactory
from aggregator.models import Feed, Entry
from aggregator.admin import update_feeds

from mock import patch, Mock

class AdminActionTests(TestCase):

	def setUp(self):
		self.feed = Mock()

	def teardown(self):
		pass

	@attr('wip')
	def test_update_feed_action_updates_feeds(self):
		update_feeds('aModelManager', 'aRequest', [self.feed])
		assert_equals(self.feed.updater.run.call_count, 1)
