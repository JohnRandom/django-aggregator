from datetime import datetime

from django.contrib import admin
from aggregator.models import Feed, Entry, ParsingError

def update_feeds(modeladmin, request, queryset):
    for feed in queryset:
    	feed.update()
update_feeds.short_description = "Update selected feeds"

class FeedAdmin(admin.ModelAdmin):
	readonly_fields = ('title', 'link', 'description', 'etag', 'language')
	list_display = ('source', 'title', 'description', 'language')
	list_filter = ('language',)
	actions = [update_feeds]
	fieldsets = (
		(None, {
			'fields': (
				'source',
				'trashed_at',
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
	list_display = ('title', 'author', 'link', 'feed', 'date_published')
	list_filter = ('feed', 'author')
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
