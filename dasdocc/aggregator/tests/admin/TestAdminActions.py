#-*- coding: utf-8 -*-
from mock import patch, Mock
from nose.tools import *
from nose.plugins.attrib import attr
from django.test import TestCase

from dasdocc.aggregator.admin import update_sources


class AdminActionTests(TestCase):

    def setUp(self):
        self.feed = Mock()

    def teardown(self):
        pass

    def test_update_feed_action_updates_feeds(self):
        update_sources('aModelManager', 'aRequest', [self.feed])
        assert_equals(self.feed.updater.run.call_count, 1)
