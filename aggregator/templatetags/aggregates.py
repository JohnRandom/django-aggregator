from django import template
from aggregator.models import Entry

register = template.Library()

@register.inclusion_tag("templatetags/aggregate_feeds.html")
def aggregate_feeds(amount):

	entries = Entry.objects.all()[:int(amount)]
	return {'entries': entries}
