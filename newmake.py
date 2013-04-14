#!/usr/bin/env python
# coding=utf-8

import re
import os
import fileinput

from os.path import basename, dirname, join
from shutil import copyfile


regex = re.compile('.*\.(mkv|mp4|avi)$')
matches = {}

for root, dirs, files in os.walk('files'):
    for name in files:
        if regex.match(name):
            f = os.path.join(root, name)
            d = dirname(dirname(f))
            try:
                matches[d].append(f)
            except KeyError:
                matches[d] = [f]


for d, files in matches.iteritems():

    index_fname = '%s/index.html' % d
    copyfile('header.html', index_fname)
    index_file = open(index_fname, 'a')

    for f in files:
        base_dir = basename(dirname(f))
        base_file = basename(f)
        movie = {
            'name': base_dir,
            'file': join(base_dir, base_file),
        }
        piece = '''
            <li class='span4'>
                <div class='thumbnail'>
                    <a href="%(file)s">
                        <img src="%(file)s.jpg" alt='' width='600'/>
                    </a>
                    <h3><a href="%(file)s">%(name)s</a></h3>
                    <a href="%(file)s-vi.srt">Phụ đề</a>
                </div>
            </li>
        ''' % movie
        index_file.write(piece)

    for line in fileinput.input('footer.html'):
        index_file.write(line)
