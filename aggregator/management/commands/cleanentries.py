from django.core.management.base import BaseCommand, CommandError
from aggregator.models import Entry

class Command(BaseCommand):
	help = 'cleanes the database from expired entries'

	def handle(self, *args, **options):
		Entry.expired.all().delete()
