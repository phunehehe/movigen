#!/usr/bin/env python
# coding=utf-8

import json
import re

from itertools import chain
from os import walk, path


INDEX_BASE = 'index.html'

MOVIE_EXTENSIONS = (
    'avi',
    'mkv',
    'mp4',
)

MOVIE_REGEX = re.compile('.*\.(%s)$' % '|'.join(MOVIE_EXTENSIONS))

with open('templates/header.html') as header_file:
    HEADER_TEMPLATE = header_file.read()

with open('templates/piece.html') as piece_file:
    PIECE_TEMPLATE = piece_file.read()

with open('templates/footer.html') as footer_file:
    FOOTER = footer_file.read()

try:
    with open('translations/active.json') as translation_file:
        TRANSLATIONS = json.load(translation_file)
except IOError:
    with open('translations/default.json') as translation_file:
        TRANSLATIONS = json.load(translation_file)


class Directory:

    def __init__(self, path):
        self.path = path
        self.directories = {}
        self.files = set()

    def add_file(self, name):
        self.files.add(name)

    def add_directory(self, name):
        try:
            new_dir = self.directories[name]
        except KeyError:
            new_dir = Directory(path.join(self.path, name))
            self.directories[name] = new_dir
        return new_dir

    def get_nearest_thumbnail(self):
        try:
            name, _ = path.splitext(next(iter(self.files)))
            return path.join('.',
                             '%s' % path.basename(self.path),
                             'thumbnails',
                             '%s.jpg' % name)
        except StopIteration:
            # Which means this directory has no file
            # Which means it must have a sub dir
            sub_dir_1_name, sub_dir_1 = next(iter(self.directories.items()))
            return path.join('.',
                             '%s' % path.basename(self.path),
                             sub_dir_1.get_nearest_thumbnail())


def add_nested_directories(directory, names):
    if not names:
        return directory
    new_path = names[0]
    new_dir = directory.add_directory(new_path)
    return add_nested_directories(new_dir, names[1:])


def apply_template(template, values):
    return template % dict(chain(TRANSLATIONS.items(), values.items()))


def path_split(p):
    '''Split a path into components'''
    head, tail = path.split(p)
    if not head:
        return [tail]
    head_parts = path_split(head)
    head_parts.append(tail)
    return head_parts


def get_subtitle_path(parent_full, file_path):
    # TODO: i18n
    subtitle_path = './%s.srt' % file_path
    if not path.isfile(path.join(parent_full, subtitle_path)):
        return ''
    return subtitle_path


def process_directory(directory):

    directory_path = directory.path

    set_name = path.basename(directory_path)
    header = apply_template(HEADER_TEMPLATE, {
        'set_name': set_name,
    })
    content = ''

    for base_sub_dir, sub_dir in sorted(directory.directories.items()):
        if len(sub_dir.files) == 1:
            base_file_path = sub_dir.files.pop()
            base_name, _ = path.splitext(base_file_path)
            movie_path = path.join(base_sub_dir, base_file_path)
            name, _ = path.splitext(movie_path)
            subtitle_path = get_subtitle_path(directory_path, name)
            thumbnail_path = path.join('.',
                                       '%s' % base_sub_dir,
                                       'thumbnails',
                                       '%s.jpg' % base_name)
        else:
            movie_path = base_sub_dir
            subtitle_path = ''
            thumbnail_path = sub_dir.get_nearest_thumbnail()
        content += apply_template(PIECE_TEMPLATE, {
            'movie_name': base_sub_dir,
            'movie_path': './%s' % movie_path,
            'subtitle_path': subtitle_path,
            'thumbnail_path': thumbnail_path,
        })

    for file_path in sorted(directory.files):

        movie_name = '%s, %s' % (set_name, file_path)
        name, _ = path.splitext(file_path)

        content += apply_template(PIECE_TEMPLATE, {
            'movie_name': movie_name,
            'movie_path': './%s' % file_path,
            'subtitle_path': get_subtitle_path(directory_path, name),
            'thumbnail_path': path.join('.',
                                        'thumbnails',
                                        '%s.jpg' % name),
        })

    with open(path.join(directory_path, INDEX_BASE), 'w') as index_file:
        index_file.write(header)
        index_file.write(content)
        index_file.write(FOOTER)

    for sub_dir in directory.directories.values():
        process_directory(sub_dir)


root_directory = Directory('.')


for root, dirs, files in walk('files', followlinks=True):
    for name in files:
        if MOVIE_REGEX.match(name):
            parts = path_split(root)
            parent_directory = add_nested_directories(root_directory, parts)
            parent_directory.add_file(name)

process_directory(root_directory)
