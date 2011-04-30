from django.contrib import admin
from aggregator.models import Feed, Entry

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
			)
		}),
	)

admin.site.register(Feed, FeedAdmin)
admin.site.register(Entry)
