from django.core.management.base import BaseCommand, CommandError
from aggregator.models import Feed

class Command(BaseCommand):
	args = '<feed_url, feed_url, ... >'
	help = 'Adds feed urls to the database'

	def handle(self, *args, **options):
		for url in args:
			feed = Feed.objects.get_or_create(source = url)

