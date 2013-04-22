#!/usr/bin/env python
# coding=utf-8

import re

from os import walk
from os.path import basename, dirname, join, isfile, split


class Directory:

    sub_dirs = {}
    files = set()

    def add_file(self, name):
        files.add(name)

    def add_sub_dir(self, sub_dir):
        if name not in sub_dirs:
            sub_dirs[name] = sub_dir

    def add_sub_dirs(self, names):
        '''Create and add a nested directory for each name in names'''
        if not names:
            return
        sub_dir = Directory()
        sub_dir.add_sub_dirs(names[1:])
        self.add_sub_dir(sub_dir)


def path_split(path):
    head, tail = split(path)
    if not head:
        return [tail]
    return path_split(head).append(tail)


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


def get_subtitle_path(parent_full, file_path):
    subtitle_path = './%s-vi.srt' % file_path
    if not isfile(join(parent_full, subtitle_path)):
        return ''
    return subtitle_path


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


def process_series(grandparent, parent, children):

    header = header_template % {
        'set_name': parent,
    }
    content = ''

    for child in sorted(children):

        movie_name = '%s, %s' % (parent, child)
        file_path = child

        content += piece_template % {
            'movie_name': movie_name,
            'movie_path': file_path,
            'subtitle_path': get_subtitle_path(join(grandparent, parent), file_path),
            'thumbnail_path': './thumbnails/%s.jpg' % file_path,
        }

    with open(join(grandparent, parent, index_base), 'w') as index_file:
        index_file.write(header)
        index_file.write(content)
        index_file.write(footer)


def generate_single_content(grandparent, parents):

    header = header_template % {
        'set_name': basename(grandparent),
    }
    content = ''

    for parent, children in sorted(parents.items()):

        if len(children) > 1:
            process_series(grandparent, parent, children)
            continue

        child = children[0]
        file_path = join(parent, child)

        content += piece_template % {
            'movie_name': parent,
            'movie_path': file_path,
            'subtitle_path': get_subtitle_path(grandparent, file_path),
            'thumbnail_path': './%s/thumbnails/%s.jpg' % (parent, child),
        }

    if not content:
        return

    with open(join(grandparent, index_base), 'w') as index_file:
        index_file.write(header)
        index_file.write(content)
        index_file.write(footer)


for root, dirs, files in walk('files', followlinks=True):
    for name in files:
        if regex.match(name):
            add_match(join(root, name))

for grandparent, parents in matches.items():
    generate_single_content(grandparent, parents)
