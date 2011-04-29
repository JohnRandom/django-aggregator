from django.core.management.base import BaseCommand, CommandError
from landing_page.models import Feed
from lib.feed_helpers import register_feed, update_feed, feed_valid

class Command(BaseCommand):
	args = '<feed_url, feed_url, ... >'
	help = 'Adds feed urls to the database'

	def handle(self, *args, **options):
		for url in args:
			feed = register_feed(url)
