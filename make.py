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
        # Assumming there is only one child
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

    for parent, children in parents.items():

        if len(children) > 1:
            is_series = True
            set_name = parent
            index_fname = '%s/%s' % (join(grandparent, parent), index_base)
            content = generate_series_content(grandparent, parent, children)
        else:
            is_series = False
            movie_name = parent
            set_name = basename(grandparent)
            index_fname = '%s/%s' % (grandparent, index_base)
            content = generate_single_content(grandparent, parents)

        header = header_template % {
            'set_name': set_name,
        }

    with open(index_fname, 'w') as index_file:
        index_file.write(header)
        index_file.write(content)
        index_file.write(footer)
