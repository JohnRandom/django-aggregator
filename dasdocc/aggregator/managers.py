from datetime import datetime, timedelta

from django.db import models

class UntrashedFeedManager(models.Manager):

    def get_query_set(self):
        return super(UntrashedFeedManager, self).get_query_set().filter(trashed_at=None)

class TrashedFeedManager(models.Manager):

    def get_query_set(self):
        return super(TrashedFeedManager, self).get_query_set().exclude(trashed_at=None)
