from django.core.management.base import BaseCommand, CommandError
from dasdocc.aggregator.models import Feed

class Command(BaseCommand):
	help = 'updates all feeds in the database'

	def handle(self, *args, **options):
		for feed in Feed.objects.all():
			feed.updater.run()
