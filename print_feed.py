#!/usr/bin/env python
import feedparser
import pprint
import sys

pp = pprint.pprint

def parse_feed(url):
  feed = feedparser.parse(url)
  pp(feed.__str__(), indent=4)


if __name__ == "__main__":
  url = sys.argv[1]
  parse_feed(url)
