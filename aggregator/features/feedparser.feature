Feature: Feedaggregator template tag
	As a site admin
	I want to to have a templatetag for the aggregator
	So that I can display feed aggregates

Scenario: Aggregating a single feed
	Given a feed with url "http://example.com/rss"
	  And an entry with title 'title-1', author 'author-1', link 'link-1' from 'today'
	  And an entry with title 'title-2', author 'author-2', link 'link-2' from 'today'
	  And an entry with title 'title-3', author 'author-3', link 'link-3' from 'today'
	 When I go to a site using the "aggregate_feeds" templatetag showing "2" results
	 Then I should see an entry with the title "title-1"
	  And I should see an entry with the title "title-2"
	  But I should not see an entry with the title "title-3"

	# title = models.CharField("Title", max_length = 255)
	# author = models.CharField("Author", max_length = 255)
	# link = models.CharField("Link", max_length = 255)
	# date_published = models.DateTimeField()
	# feed = models.ForeignKey(Feed)