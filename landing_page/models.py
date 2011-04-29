from django.db import models

class Feed(models.Model):

	title = models.CharField("Title", max_length = 255, null = True, blank = True)
	link = models.URLField("Link", max_length = 255)
	description = models.CharField("Description", max_length = 255, null = True, blank = True)
	etag = models.CharField("ETag", max_length = 255, null = True, blank = True)
	date_parsed = models.DateTimeField("Last visited", auto_now = True)

	def __unicode__(self):
		return unicide(self.title or self.link)

	@models.permalink
	def get_absolute_url(self):
		raise NotImplementedError()
