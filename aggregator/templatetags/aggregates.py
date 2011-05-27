try: from settings import aggregate_feeds_template
except ImportError: from aggregator.aggregator_settings import aggregate_feeds_template

import ttag
from django import template
from django.conf import settings
from aggregator.models import Feed, Entry, StaticContent as StaticContentModel

register = template.Library()

class TemplateRenderingTag(ttag.Tag):

	template = None

	def render(self, context):
		output = self.output(self.resolve(context))
		if self.template is not None:
			return template.loader.render_to_string(self.template, output)
		else:
			return output

class AggregateFeeds(TemplateRenderingTag):

	limit = ttag.Arg(keyword = True, default = 0)
	template = aggregate_feeds_template

	def output(self, data):
		limit = data.get('limit', 0)

		if limit > 0:
			entries = Entry.objects.all()[:limit]
		else:
			entries = Entry.objects.all()

		return {'entries': entries}
register.tag(AggregateFeeds)

class StaticContent(ttag.Tag):

	identifier = ttag.Arg()

	def output(self, data):
		identifier = data.get('identifier')
		try: content = StaticContentModel.objects.get(name = identifier)
		except StaticContentModel.DoesNotExist: return u''

		return u'\n'.join([sel.bound_content for sel in content.selector_set.all()])
register.tag(StaticContent)