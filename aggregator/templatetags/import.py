import os
from glob import glob

from django import template
from django.conf import settings

register = template.Library()
STATIC_URL = settings.STATIC_URL
CSS_ROOT = os.path.join(settings.STATIC_URL, 'css/')
LINK_TAG = '<link href="%s" rel="stylesheet" type="text/css">'

@register.simple_tag
def all_stylesheets():
	return stylesheets('.')

@register.simple_tag
def stylesheets(directory):
	links = []

	root = os.path.join(CSS_ROOT, os.path.normpath(directory), '*.css')
	for css_file in glob(root):
		if not os.path.isfile(css_file): continue
		ressource_url = settings.MEDIA_URL + os.path.relpath(css_file, STATIC_URL)
		links.append(LINK_TAG % ressource_url)

	return '\n'.join(links)