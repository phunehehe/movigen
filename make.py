#!/usr/bin/env python
# coding=utf-8

import re
import os

from os.path import basename, dirname, join


regex = re.compile('.*\.(mkv|mp4|avi)$')
matches = {}

for root, dirs, files in os.walk('files', followlinks=True):
    for name in files:
        if regex.match(name):
            f = os.path.join(root, name)
            d = dirname(dirname(f))
            try:
                matches[d].append(f)
            except KeyError:
                matches[d] = [f]


for d, files in matches.items():

    with open('header.html') as header_file:
        header = header_file.read() % {
            'set_name': basename(d)
        }

    with open('piece.html') as piece_file:
        piece_template = piece_file.read()

    with open('footer.html') as footer_file:
        footer = footer_file.read()

    content = ''

    for f in sorted(files):

        base_dir = basename(dirname(f))
        file_path = join(base_dir, basename(f))

        content += piece_template % {
            'movie_name': base_dir,
            'movie_path': file_path,
            'subtitle_path': './%s-vi.srt' % file_path,
            'thumbnail_path': './%s.jpg' % file_path,
        }

    index_fname = '%s/index.html' % d

    with open(index_fname, 'w') as index_file:
        index_file.write(header)
        index_file.write(content)
        index_file.write(footer)
