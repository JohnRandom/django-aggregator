#-*- coding: utf-8 -*-
from nose.tools import *
from django.test import TestCase
from nose.plugins.attrib import attr
from mock import patch, Mock

from aggregator.lib.updaters.static_content_updater import _StaticContentUpdater

FailingStaticContentParser = Mock(side_effect = IOError)

class PublicInterfaceTests(TestCase):

	def setUp(self):
		pass

	def teardown(self):
		pass

	@patch('aggregator.lib.updaters.static_content_updater.StaticContentParser')
	def test_updater_run_should_call_the_appropriate_parser_methods(self, ParserClass):
		updater = _StaticContentUpdater(Mock())
		updater.run()

		parser = ParserClass.return_value
		assert_equals(parser.process_nodes.call_count, 1)

	def test_parsing_errors_should_be_handled_quietly(self):
		mocked_instance = Mock()
		updater = _StaticContentUpdater(mocked_instance)
		mocked_instance.log_error.called_once_with(IOError)

	@raises(TypeError)
	def test_parser_should_raise_type_error_on_non_instance_method_run(self):
		updater = _StaticContentUpdater(None)
		updater.run()

	@raises(TypeError)
	def test_parser_should_raise_type_error_on_non_instance_method_clean(self):
		updater = _StaticContentUpdater(None)
		updater.clean()

	def test_parser_should_delete_the_correct_data_on_clean(self):
		mocked_instance = Mock()
		updater = _StaticContentUpdater(mocked_instance)
		updater.clean()

		assert_equals(mocked_instance.get_expired_entries.call_count, 1)
		assert_equals(mocked_instance.get_expired_entries().delete.call_count, 1)