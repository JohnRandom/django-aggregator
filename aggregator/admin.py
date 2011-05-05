from django.contrib import admin
from aggregator.models import Feed, Entry, ParsingError

class FeedAdmin(admin.ModelAdmin):
	fieldsets = (
		(None, {
			'fields': (
				'source',
			)
		}),
		('Extracted attributes', {
			'classes': (
				'collapse',
			),
			'fields': (
				'title',
				'link',
				'description',
				'etag',
				'language',
			)
		}),
	)

admin.site.register(Feed, FeedAdmin)
admin.site.register(Entry)
admin.site.register(ParsingError)
