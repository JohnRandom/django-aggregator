from datetime import datetime, timedelta
from aggregator.lib.static_content_helpers import StaticContentParser

def requires_instance(method):
	def wrapper(self, *args, **kwargs):
		if self.instance is None:
			raise TypeError("Can't call %s with a non-instance manager" % method.__name__)
		else:
			return method(self, *args, **kwargs)
	return wrapper

class StaticContentUpdater(object):

	def __get__(self, instance, model):
		if instance is not None and instance.pk is None:
			raise ValueError("%s objects need to have a primary key value "
				"before you can access their updaters." % model.__name__)
		updater = _StaticContentUpdater(instance)
		return updater

	def contribute_to_class(self, cls, name):
		setattr(cls, name, self)

class _StaticContentUpdater(object):

	def __init__(self, instance):
		self.instance = instance

	@requires_instance
	def run(self):
		parser = StaticContentParser(self.instance)
		parser.process_nodes()
		return True

	@requires_instance
	def clean(self):
		self.instance.get_expired_entries().delete()
