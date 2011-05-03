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
		}

	def figure_date(self):
		'''
		Tries to guess the date the entry was published. It first looks into the
		'published' date, then into the 'created' date and finally sets the current
		date, if no other field was set.
		'''

		m = self.entry

		if hasattr(m, 'published'): date = m.published
		elif hasattr(m, 'created'): date = m.created
		elif hasattr(m, 'updated'): date = m.updated
		else: date = datetime.now()
		return date

	def get_defaults(self):
		'''
		Provides the fields necessary for Feed creation as dictionary.
		'''
		return self._map_content()
