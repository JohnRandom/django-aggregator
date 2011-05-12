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

	def _parse_data(self):
		self.data = html.parse(self.desc.source)

	def _parse_nodes(self, selector):
		sel = CSSSelector(selector.css_selector)
		nodes = self._process_content(sel(self.data))
		selector.bound_content = self._stringify_nodes(nodes)
		selector.save()
		return selector.bound_content

	def _process_content(self, content):
		return content

	def _stringify_nodes(self, nodes):
		return ''.join( [etree.tostring(node) for node in nodes] )

	@data_required
	def get_nodes(self):
		return [self._parse_nodes(selector) for selector in self.selectors]

	@data_required
	def process_nodes(self):
		self.get_nodes()
