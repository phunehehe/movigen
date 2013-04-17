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

    with open('templates/header.html') as header_file:
        header = header_file.read() % {
            'set_name': basename(d)
        }

    with open('templates/piece.html') as piece_file:
        piece_template = piece_file.read()

    with open('templates/footer.html') as footer_file:
        footer = footer_file.read()

    content = ''

    for f in sorted(files):

        # Count the number of movie files in the same dir. If there are more
        # than one, we are dealing with a series
        parent_dir = dirname(f)
        count = 0
        is_series = False
        for name in os.listdir(parent_dir):
            if regex.match(name):
                count += 1
                if count > 1:
                    is_series = True
                    break

        parent_name = basename(parent_dir)
        f_name = basename(f)
        file_path = join(parent_name, f_name)
        movie_name = '%s, %s' % (parent_name, f_name) if is_series else parent_name

        content += piece_template % {
            'movie_name': movie_name,
            'movie_path': file_path,
            'subtitle_path': './%s-vi.srt' % file_path,
            'thumbnail_path': './%s.jpg' % file_path,
        }

    index_fname = '%s/index.html' % d

    with open(index_fname, 'w') as index_file:
        index_file.write(header)
        index_file.write(content)
        index_file.write(footer)
