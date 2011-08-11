from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError
from dasdocc.aggregator.models import Feed

class Command(BaseCommand):
    help = 'cleanes the database from expired entries'

    def handle(self, *args, **options):
        for feed in Feed.objects.all():
            feed.get_expired_entries().delete()
