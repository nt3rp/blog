#!/bin/python2
from re import sub
from os import listdir, remove
from os.path import isfile, join

from slugify import slugify

DEFAULT_OLD_EXTENSION = '.markdown'
DEFAULT_NEW_EXTENSION = '.md'
DEFAULT_PATH = './content'
DEFAULT_FILES = [ join(DEFAULT_PATH,f) for f in listdir(DEFAULT_PATH) if isfile(join(DEFAULT_PATH,f)) ]

OLD_EXT = DEFAULT_OLD_EXTENSION
OLD_EXT_REGEX = r'{0}$'.format(OLD_EXT)

NEW_EXT = DEFAULT_NEW_EXTENSION
FILES = filter(lambda f: f.endswith(OLD_EXT), DEFAULT_FILES)

for filename in FILES:
    new_file = sub(OLD_EXT_REGEX, NEW_EXT, filename)
    print('Processing {0}'.format(filename))
    with open(filename, 'r') as old, open(new_file, 'a') as new:
        for line in old.readlines():
            if line.startswith('title: '):
                old_title = line.split('title:')[1].strip()[1:-1]
                new_title = u'title: {0}\r\n'.format(old_title)
                slug = u'slug: {0}\r\n'.format(slugify(old_title))
                new.write(new_title)
                new.write(slug)
            elif not line.startswith('---'):
                new.write(line)
                
for filename in FILES:
    print('Deleting {0}'.format(filename))
    remove(filename)


