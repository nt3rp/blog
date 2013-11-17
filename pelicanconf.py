#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# --- General Settings ---
AUTHOR = u'Nicholas Terwoord'
SITENAME = u'NT3R'
SITESUBTITLE=u'A blog that needs work'
SITEURL = ''
TIMEZONE = 'Europe/Paris'
DEFAULT_LANG = u'en'
THEME = 'themes/pelican-octopress-theme'
DISQUS_SITENAME='nt3rp'
DEFAULT_PAGINATION = 10
# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# --- Navigation ---
MENUITEMS = [
    ('Archives', 'archives.html')
]

# --- Sidebar --- 
LINKS =  (('Pelican', 'http://getpelican.com/'),
          ('Python.org', 'http://python.org/'),
          ('Jinja2', 'http://jinja.pocoo.org/'),
          ('You can modify those links in your config file', '#'),)

SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

# --- Theme-specific Settings ---
GITHUB_USER = u'nt3rp'
GITHUB_REPO_COUNT = 5
GITHUB_SKIP_FORK = True
GITHUB_SHOW_USER_LINK = True
# INLINE_DISQUSSIONS = True

# --- Plugin Settings ---
PLUGIN_PATH = 'plugins'
PLUGINS = [
    'liquid_tags.img',
    'liquid_tags.video',
    'liquid_tags.youtube',
    'liquid_tags.include_code',
]

# --- Source Settings ---
PATH='content'
STATIC_PATHS = ['images', ]

# --- Paths and URIs ---
ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

# --- RSS Settings ---
# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
