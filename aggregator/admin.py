from django.contrib import admin
from aggregator.models import Feed, Entry, ParsingError

class FeedAdmin(admin.ModelAdmin):
	readonly_fields = ('title', 'link', 'description', 'etag', 'language')
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

class EntryAdmin(admin.ModelAdmin):
	readonly_fields = ('author', 'date_published', 'feed', 'link')
	fieldsets = (
		(None, {
			'fields': (
				'title',
				'tags',
			)
		}),
		('Read only', {
			'classes': (
				'collapse',
			),
			'fields': (
				'author',
				'date_published',
				'link',
				'feed',
			)
		}),
	)

class ParsingErrorAdmin(admin.ModelAdmin):
	readonly_fields = ('feed', 'error_message', 'date_raised')

admin.site.register(Feed, FeedAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(ParsingError, ParsingErrorAdmin)
