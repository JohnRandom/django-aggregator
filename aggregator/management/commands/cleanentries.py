from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError
from aggregator.models import Feed

class Command(BaseCommand):
	help = 'cleanes the database from expired entries'

	def handle(self, *args, **options):
		for feed in Feed.objects.all():
			threshold = datetime.now() - timedelta(days = feed.content_expiration)
			feed.entry_set.filter( date_published__lte = threshold ).delete()
