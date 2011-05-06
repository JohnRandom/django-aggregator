from datetime import timedelta, datetime
from django.core.management.base import BaseCommand, CommandError
from aggregator.models import Feed

try: from settings import TRASH_EXPIRATION
except ImportError: from aggregator.aggregator_settings import TRASH_EXPIRATION

class Command(BaseCommand):
	help = 'trashes all invalid feeds'

	def handle(self, *args, **options):
		delta = timedelta(seconds = TRASH_EXPIRATION)
		treshold = datetime.now() - delta

		Feed.trashed.filter(trashed_at__lte = treshold).delete()
