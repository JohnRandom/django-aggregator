from datetime import datetime, timedelta

from lettuce import *
from lxml import html
from django.test.client import Client
from nose.tools import *
from lettuce.django import django_url
from django.core.management import call_command

from aggregator.models import Feed, Entry
from aggregator.templatetags.aggregates import aggregate_feeds

@step(u'a feed with url "(.*)"')
def a_feed_with_url_feed_url(step, feed_url):
	world.feed = Feed.objects.create(source = feed_url)

@step(u'an entry with title \'(.*)\', author \'(.*)\', link \'(.*)\' from \'(.*)\'')
def and_an_entry_with_title_author_link_from(step, title, author, link, date_description):
	if date_description == 'today':
		_date = datetime.now()
	world.feed.entry_set.create(title = title, author = author, link = link, date_published = _date)

@step(u'I go to a site using the "aggregate_feeds" templatetag showing "(.*)" results')
def i_go_to_a_site_using_the_group1_templatetag_showing_group2_results(step, number_of_entries):
	if type(number_of_entries) != int and number_of_entries != 'all':
		number_of_entries = int(number_of_entries)
	world.entries = aggregate_feeds(number_of_entries)

@step(u'I should see an entry with the title "(.*)"')
def i_should_see_an_entry_with_title(step, title):
	assert_true( any([title == entry.title for entry in world.entries['entries']]),
		"could not find %s in %s" %(title, str(world.entries)) )

@step(u'I should not see an entry with the title "(.*)"')
def i_should_not_see_an_entry_with_the_title(step, title):
	assert_false( any([title == entry.title for entry in world.entries['entries']]),
		"found %s in %s" %(title, str(world.entries)) )
