from datetime import datetime

class EntryWrapper(object):

	def __init__(self, entry_instance, feed_instance):
		self.model = entry_instance
		self.feed = feed_instance

	def _map_content(self):
		m, f = self.model, self.feed

		date = self.figure_date()

		return {
			'title': m.title,
			'feed': f,
			'date_published': date,
			'author': m.get('author', 'unknown'),
		}

	def figure_date(self):
		m = self.model

		if hasattr(m, 'published_parsed'): date = m.published_parsed
		elif hasattr(m, 'created_parsed'): date = m.created_parsed
		else: date = datetime.now()
		return date

	def get_defaults(self):
		return self._map_content()
