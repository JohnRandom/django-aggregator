from lettuce import *
from lxml import html
from django.test.client import Client
from nose.tools import *
from lettuce.django import django_url

@step(r'I got to "(.*)"')
def access_url(step, url):
	abs_url = django_url(url)
    response = world.browser.get(abs_url)
    world.dom = html.fromstring(response.content)

@step(r'I should see "(.*)"')
def see_header(step, element):
    header = world.dom.cssselect(element)
    assert header.text == text