from datetime import datetime

from django.contrib import admin
from dasdocc.aggregator.models import Feed, Entry, ParsingError, StaticContent, Selector, StaticContentError, SourceCategory
from dasdocc.aggregator.forms import StaticContentForm

def update_sources(modeladmin, request, queryset):
    for source in queryset:
        source.updater.run()
update_sources.short_description = "Update selected sources"

class ParsingErrorInline(admin.TabularInline):
    extra = 0
    model = ParsingError
    readonly_fields = ('feed', 'error_message', 'date_raised')

class EntryInline(admin.StackedInline):
    extra = 0
    model = Entry
    readonly_fields = ('title', 'author', 'date_published', 'feed', 'link')
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


class FeedAdmin(admin.ModelAdmin):
    readonly_fields = ('title', 'link', 'description', 'etag', 'language',
        'trashed_at')
    list_display = ('source', 'title', 'description', 'language',
        'content_expiration', 'is_ok')
    list_filter = ('language',)
    actions = [update_sources]
    inlines = [EntryInline, ParsingErrorInline]
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


class SelectorInline(admin.StackedInline):
    model = Selector
    fields = ('name', 'css_selector', 'max_amount_of_childs', 'bound_content')
    readonly_fields = ('bound_content',)
    extra = 0


class StaticContentErrorInline(admin.TabularInline):
    model = StaticContentError
    readonly_fields = ('error', 'message', 'date_raised')
    extra = 0
    can_delete = False


class StaticContentAdmin(admin.ModelAdmin):
    inlines = [SelectorInline, StaticContentErrorInline]
    actions = [update_sources]
    form = StaticContentForm
    list_display = ('name', 'source', 'is_ok', 'date_parsed')
    readonly_fields = ('date_parsed',)


admin.site.register(Feed, FeedAdmin)
admin.site.register(StaticContent, StaticContentAdmin)
admin.site.register(SourceCategory)
