import time
from datetime import datetime

class EntryWrapper(object):
	'''
	This is a thin wrapper for the entries of a feed, which allows easy access
	to a subset of the entry properties suitable to create an Entry instance.
	'''

	def __init__(self, entry_obj):
		self.entry = entry_obj

	def _map_content(self):
		m = self.entry

		return {
			'title': m.title,
			'date_published': self.figure_date(),
			'author': m.get('author', 'unknown'),
			'link': m.get('link', None)
		}

	def figure_date(self):
		'''
		Tries to guess the date the entry was published. It first looks into the
		'published' date, then into the 'created', then into 'updated' date and
		finally sets the current date, if no other field was set.
		'''

		m = self.entry

		if hasattr(m, 'published_parsed'): date = m.published_parsed
		elif hasattr(m, 'created_parsed'): date = m.created_parsed
		elif hasattr(m, 'updated_parsed'): date = m.updated_parsed
		# always return the current time as default
		else: date = time.localtime()
		return datetime.fromtimestamp(time.mktime(date))
		#return time.strftime('%Y-%m-%d %H:%M:%S', date)

	def get_defaults(self):
		'''
		Provides the fields necessary for Feed creation as dictionary.
		'''
		return self._map_content()

	def get_tags(self):
		tags = self.entry.get('tags', [])
		return [tag['term'] for tag in tags]
