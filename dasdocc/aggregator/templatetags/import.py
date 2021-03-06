import os
from glob import glob

from django import template
from django.conf import settings

register = template.Library()
STATIC_ROOT = settings.STATIC_ROOT
CSS_ROOT = os.path.join(settings.STATIC_ROOT, 'css/')
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
        ressource_url = '/%s' % os.path.relpath(css_file)
        links.append(LINK_TAG % ressource_url)

    return '\n'.join(links)