from datetime import datetime, timedelta
from aggregator.lib.feed_helpers import FeedParser

def requires_instance(method):
	def wrapper(self, *args, **kwargs):
		if self.instance is None:
			raise TypeError("Can't call %s with a non-instance manager" % method.__name__)
		else:
			return method(self, *args, **kwargs)
	return wrapper

def untrashed_only(method):
	def wrapper(self, *args, **kwargs):
		if hasattr(self.instance, 'trashed_at') and self.instance.trashed_at is None:
			return method(self, *args, **kwargs)
		else:
			return False
	return wrapper

class FeedUpdater(object):

	def __get__(self, instance, model):
		if instance is not None and instance.pk is None:
			raise ValueError("%s objects need to have a primary key value "
				"before you can access their updaters." % model.__name__)
		updater = _FeedUpdater(instance)
		return updater

	def contribute_to_class(self, cls, name):
		setattr(cls, name, self)

class _FeedUpdater(object):

	def __init__(self, instance):
		self.instance = instance

	def _is_entry_expired(self, wrapped_entry):
		return wrapped_entry.get_defaults()['date_published']\
				< datetime.now() - timedelta(days = self.instance.content_expiration)

	@requires_instance
	@untrashed_only
	def run(self):
		parser = FeedParser(self.instance)
		defaults = parser.get_defaults()

		# update instance
		if parser.feed.get('status', False) == 304: return True
		self.instance.__dict__.update(**defaults)
		self.instance.save()

		# update entries
		for entry in parser.get_entries():
			if self._is_entry_expired(entry): continue
			e, new = self.instance.entry_set.get_or_create(**entry.get_defaults())
			e.tags.set(*entry.get_tags())
			e.save()

		# create parsing errors if necessary
		if parser.error['raised']:
			self.instance.parsingerror_set.create(error_message = parser.error['message'][:255])

		# validate and trash if necessary
		self.instance.valid = parser.is_valid()
		if not self.instance.valid and self.instance.trashed_at is None: self.instance.trashed_at = datetime.now()
		self.instance.save()
		return self.instance.valid

	@requires_instance
	def clean(self):
		self.instance.get_expired_entries().delete()
