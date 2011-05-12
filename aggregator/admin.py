from datetime import datetime

from django.contrib import admin
from aggregator.models import Feed, Entry, ParsingError, StaticContent, Selector, StaticContentError
from aggregator.forms import StaticContentForm

def update_feeds(modeladmin, request, queryset):
    for feed in queryset:
    	feed.updater.run()
update_feeds.short_description = "Update selected sources"

class FeedAdmin(admin.ModelAdmin):
	readonly_fields = ('title', 'link', 'description', 'etag', 'language', 'trashed_at')
	list_display = ('source', 'title', 'description', 'language', 'content_expiration',)
	list_filter = ('language',)
	actions = [update_feeds]
	fieldsets = (
		(None, {
			'fields': (
				'source',
				'content_expiration',
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
				'trashed_at',
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
	list_display = ('feed', 'error_message', 'date_raised',)
	list_filter = ('feed__source', 'error_message',)


class SelectorInline(admin.StackedInline):
	model = Selector
	fields = ('name', 'css_selector', 'bound_content')
	readonly_fields = ('bound_content',)

class StaticContentErrorInline(admin.TabularInline):
	model = StaticContentError
	readonly_fields = ('error', 'message', 'date_raised')

class StaticContentAdmin(admin.ModelAdmin):
	inlines = [ SelectorInline, StaticContentErrorInline]
	actions = [ update_feeds ]
	form = StaticContentForm
	list_display = ('name', 'source', 'is_ok', 'date_parsed')
	readonly_fields = ('date_parsed',)


admin.site.register(Feed, FeedAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(ParsingError, ParsingErrorAdmin)
admin.site.register(StaticContent, StaticContentAdmin)
