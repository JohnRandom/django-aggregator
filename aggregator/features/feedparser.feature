Feature: Feedaggregator template tag
	As a site admin
	I want to to have a templatetag for the aggregator
	So that I can display feed aggregates

Scenario: Aggregating a single feed
	Given a feed with url "http://example.com/rss"
	  And the feed has the following entries
	 When I go to a site using the "aggregate_feeds" templatetag showing "3" results
	 Then I should see
	