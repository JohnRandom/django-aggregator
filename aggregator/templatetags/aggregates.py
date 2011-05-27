try: from settings import aggregate_feeds_template
except ImportError: from aggregator.aggregator_settings import aggregate_feeds_template

from django import template
from django.conf import settings
from aggregator.models import Feed, Entry, StaticContent

register = template.Library()

@register.inclusion_tag(aggregate_feeds_template)
def aggregate_feeds(amount):
	if type(amount) == int:
		entries = Entry.objects.all()[:int(amount)]
	elif (isinstance(amount, SafeUnicode) or type(amount) == unicode) and amount == 'all':
		entries = Entry.objects.all()
	else:
		raise Exception("'amount' must be an instance of SafeUnicode, found %s instead" % amount.__class__.__name__)

	return {'entries': entries}

@register.simple_tag
def static_content(identifier):
	try: content = StaticContent.objects.get(name = identifier)
	except StaticContent.DoesNotExist: return u''

	return u'\n'.join([sel.bound_content for sel in content.selector_set.all()])

import ttag

class TemplateRenderingTag(ttag.Tag):

	template = None

	def render(self, context):
		output = self.output(self.resolve(context))
		if self.template is not None:
			return template.loader.render_to_string(self.template, output)
		else:
			return output

class AggregateFeeds(TemplateRenderingTag):

	class Meta:
		name = 'aggregatefeeds'

	limit = ttag.Arg(keyword = True)
	template = aggregate_feeds_template

	def output(self, data):
		limit = data.get('limit', 0)

		if limit > 0:
			entries = Entry.objects.all()[:limit]
		else:
			entries = Entry.objects.all()

		return {'entries': entries}
register.tag(AggregateFeeds)