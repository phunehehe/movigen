#!/usr/bin/env python
# coding=utf-8

import re

from os import walk
from os.path import basename, dirname, join


index_base = 'index.html'
matches = {
#   '/root/grandparent': {
#       'parent': [
#           'file1',
#           'file2',
#       ]
#   }
}
regex = re.compile('.*\.(mkv|mp4|avi)$')


with open('templates/header.html') as header_file:
    header_template = header_file.read()

with open('templates/piece.html') as piece_file:
    piece_template = piece_file.read()

with open('templates/footer.html') as footer_file:
    footer = footer_file.read()


def add_match(child_full):

    child = basename(child_full)
    parent_full = dirname(child_full)

    parent = basename(parent_full)
    grandparent = dirname(parent_full)

    if grandparent not in matches:
        matches[grandparent] = {parent: [child]}
    else:
        mg = matches[grandparent]
        if parent not in mg:
            mg[parent] = [child]
        else:
            mg[parent].append(child)


def generate_series_content(grandparent, parent, children):

    content = ''

    for child in children:

        movie_name = '%s, %s' % (parent, child)
        file_path = child

        content += piece_template % {
            'movie_name': movie_name,
            'movie_path': file_path,
            'subtitle_path': './%s-vi.srt' % file_path,
            'thumbnail_path': './%s.jpg' % file_path,
        }

    return content


def generate_single_content(grandparent, parents):

    content = ''

    for parent, children in parents.items():

        if len(children) > 1:
            print('Fancy stuff needed for %s, %s' % (grandparent, parent))
            continue

        child = children[0]
        file_path = join(parent, child)

        content += piece_template % {
            'movie_name': parent,
            'movie_path': file_path,
            'subtitle_path': './%s-vi.srt' % file_path,
            'thumbnail_path': './%s.jpg' % file_path,
        }

    return content


for root, dirs, files in walk('files', followlinks=True):
    for name in files:
        if regex.match(name):
            add_match(join(root, name))


for grandparent, parents in matches.items():

    header = header_template % {
        'set_name': basename(grandparent),
    }
    content = generate_single_content(grandparent, parents)

    with open(join(grandparent, index_base), 'w') as index_file:
        index_file.write(header)
        index_file.write(content)
        index_file.write(footer)
