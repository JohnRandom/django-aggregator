#-*- coding: utf-8 -*-
import time
from datetime import datetime
from nose.tools import *
from django.test import TestCase
from nose.plugins.attrib import attr
from mock import Mock, patch

from dasdocc.aggregator.lib.static_content_helpers import StaticContentParser
from dasdocc.aggregator.tests.factories import StaticContentMock, static_content_parsed, SelectorMock

class InterfaceTests(TestCase):
	'''
	Tests the public interface of the parser and asserts that the underlying implementation
	is called correctly. It is not testing any actual content processing.
	'''

	def setUp(self):
		self.static_content_mock = StaticContentMock()
		self.static_content_mock.selector_set.all = Mock(return_value = [])
		self.parser = StaticContentParser(self.static_content_mock)

	def teardown(self):
		pass

	@patch('dasdocc.aggregator.lib.static_content_helpers.html.parse')
	def test_parser_should_collect_data_during_get_nodes(self, parse):
		self.parser.get_nodes()
		parse.assert_called_once_with('http://mocked.source/')

	@patch('dasdocc.aggregator.lib.static_content_helpers.html.parse')
	def test_parser_should_collect_data_during_process_nodes(self, parse):
		self.parser.process_nodes()
		parse.assert_called_once_with('http://mocked.source/')

	@patch('dasdocc.aggregator.lib.static_content_helpers.html.parse')
	def test_parser_should_parse_data_only_once(self, parse):
		self.parser.process_nodes()
		self.parser.get_nodes()
		self.parser.process_nodes()
		self.parser.get_nodes()
		parse.assert_called_once_with('http://mocked.source/')

mocked_datetime = Mock()
mocked_datetime.now = Mock(return_value = 'time')
class ContentProcessingTests(TestCase):
	'''
	Tests the correct processing of data.
	'''

	def setUp(self):
		selector = SelectorMock()
		self.static_content_mock = StaticContentMock()
		self.static_content_mock.selector_set.all = Mock(return_value = [selector])
		self.parser = StaticContentParser(self.static_content_mock)
		self.parser.data = static_content_parsed

	def teardown(self):
		self.parser.data = None

	def test_selector_data_is_processed_correclty(self):
		processed_nodes = self.parser.get_nodes()
		assert_true( '<div id="content">' in processed_nodes[0])

	def test_links_in_nodes_are_made_absolute(self):
		processed_nodes = self.parser.get_nodes()
		assert_true('<a href="http://mocked.source/test">' in processed_nodes[0])

	@patch('dasdocc.aggregator.lib.static_content_helpers.datetime', new = mocked_datetime)
	def test_processing_time_is_assigned_to_staticcontent_object(self):
		parser = StaticContentParser(self.static_content_mock)
		assert_equals(parser.desc.date_parsed, 'time')