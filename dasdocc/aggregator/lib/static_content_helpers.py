from datetime import datetime

from lxml import etree, html
from lxml.cssselect import CSSSelector
from lxml.html.clean import clean_html

def data_required(method):
    def wrapper(self, *args, **kwargs):
        if self.data is None:
            self._parse_data()
        return method(self, *args, **kwargs)
    return wrapper

class StaticContentParser(object):

    def __init__(self, static_content):
        self.static_content = static_content
        self.selectors = static_content.selector_set.all()
        self.data = None

        self.static_content.date_parsed = datetime.now()
        self.static_content.save()

    def _parse_data(self):
        html_ = html.parse(self.static_content.source)
        self.data = clean_html(html_)

    def _parse_nodes(self, selector):
        sel = CSSSelector(selector.css_selector)

        nodes = sel(self.data)
        nodes = map(self._rewrite_ids_to_class, nodes)
        nodes = self._nodes_to_string(nodes)
        nodes = self._proccess_string_nodes(nodes)

        selector.bound_content = ''.join(nodes)
        selector.save()
        return selector.bound_content

    def _rewrite_ids_to_class(self, root):
        for node in root.iter():
            self._rewrite_ids_on_node(node)
        self._rewrite_ids_on_node(root)
        return root

    def _rewrite_ids_on_node(self, node):
        if 'id' in node.attrib.keys():
            if not node.attrib.has_key('class'):
                node.attrib['class'] = 'id-%s' % node.attrib['id']
            else:
                node.attrib['class'] += ' id-%s' % node.attrib['id']
            del node.attrib['id']

    def _proccess_string_nodes(self, content):
        return [html.make_links_absolute(node, self.static_content.source)
            for node in content]

    def _nodes_to_string(self, nodes):
        return [etree.tostring(node) for node in nodes]

    @data_required
    def get_nodes(self):
        return [self._parse_nodes(selector) for selector in self.selectors]

    @data_required
    def process_nodes(self):
        self.get_nodes()

