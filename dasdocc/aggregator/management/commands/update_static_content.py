from django.core.management.base import BaseCommand, CommandError
from dasdocc.aggregator.models import StaticContent

class Command(BaseCommand):
    help = 'updates all ststic content sources in the database'

    def handle(self, *args, **options):
        for source in StaticContent.objects.all():
            source.updater.run()
