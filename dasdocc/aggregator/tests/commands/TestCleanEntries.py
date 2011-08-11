#-*- coding: utf-8 -*-
from datetime import datetime, timedelta

from nose.tools import *
from django.test import TestCase
from nose.plugins.attrib import attr

from django.core.management import call_command as call

from dasdocc.aggregator.tests.factories import EntryFactory
from dasdocc.aggregator.models import Entry

class CleanEntryTests(TestCase):

    def setUp(self):
        delta = timedelta(days=8)
        publish_date = datetime.now() - delta
        self.entry = EntryFactory(date_published=publish_date)

    def teardown(self):
        pass

    def test_clean_up_should_remove_expired_entries(self):
        self.entry.feed.content_expiration = 7
        self.entry.feed.save()

        assert_equals(Entry.objects.count(), 1)
        call('cleanentries')
        assert_equals(Entry.objects.count(), 0)

    def test_clean_up_should_not_remove_entries_not_yet_expired(self):
        self.entry.feed.content_expiration = 14
        self.entry.feed.save()

        assert_equals(Entry.objects.count(), 1)
        call('cleanentries')
        assert_equals(Entry.objects.count(), 1)
