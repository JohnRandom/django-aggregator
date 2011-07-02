from datetime import datetime
from lxml import etree, html
from lxml.cssselect import CSSSelector

def data_required(method):
	def wrapper(self, *args, **kwargs):
		if self.data is None:
			self._parse_data()
		return method(self, *args, **kwargs)
	return wrapper

class StaticContentParser(object):

	def __init__(self, content_obj):
		self.desc = content_obj
		self.selectors = content_obj.selector_set.all()
		self.data = None
		self.node_processors = {'before': [], 'after': []}

		self.desc.date_parsed = datetime.now()
		self.desc.save()

	def _parse_data(self):
		self.data = html.parse(self.desc.source)

	def _parse_nodes(self, selector):
		sel = CSSSelector(selector.css_selector)
		nodes = sel(self.data)

		for func in self.node_processors['before']:
			nodes = func(nodes)

		nodes = self._stringify_nodes(sel(self.data))
		nodes = self._process_str_content(nodes)

		for func in self.node_processors['after']:
			nodes = func(nodes)

		selector.bound_content = ''.join(nodes)
		selector.save()
		return selector.bound_content

	def _process_str_content(self, content):
		return [html.make_links_absolute(node, self.desc.source) for node in content]

	def _stringify_nodes(self, nodes):
		return [etree.tostring(node) for node in nodes]

	@data_required
	def get_nodes(self):
		return [self._parse_nodes(selector) for selector in self.selectors]

	@data_required
	def process_nodes(self):
		self.get_nodes()

	def register(self, processor, timing = 'before_stringify'):
		'''
		Registers function to be executed either before or after the string conversion
		of the nodes.
			before_stringify (default): def func(node_list) <as etree elements>
			after_stringify: def func(node_list) <as stings>
		'''
		if not callable(processor):
			raise TypeError('Node processors need to be functions')

		if timing == 'before_stringify':
			self.node_processors['before'].append(processor)
		elif timing == 'after_stringify':
			self.node_processors['after'].append(processor)
		else:
			raise ValueError('Unknown timing "%s", expected: [before_stringify, after_stringify]')

