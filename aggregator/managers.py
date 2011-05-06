from datetime import datetime, timedelta

from django.db import models

try: from settings import ENTRY_EXPIRATION_DAYS
except ImportError: from aggregator.aggregator_settings import ENTRY_EXPIRATION_DAYS

class UntrashedFeedManager(models.Manager):

	def get_query_set(self):
		return super(UntrashedFeedManager, self).get_query_set().filter(trashed_at = None)

class TrashedFeedManager(models.Manager):

	def get_query_set(self):
		return super(TrashedFeedManager, self).get_query_set().exclude(trashed_at = None)

class ExpiredEntriesManager(models.Manager):

	def get_query_set(self):
		delta = timedelta(days = ENTRY_EXPIRATION_DAYS)
		treshold = datetime.now() - delta
		return super(ExpiredEntriesManager, self).get_query_set().filter(date_published__lte = treshold)
