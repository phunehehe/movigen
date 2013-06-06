#!/usr/bin/env python
# coding=utf-8

import re

from os import walk, path


INDEX_BASE = 'index.html'
MOVIE_EXTENSIONS = (
    'avi',
    'mkv',
    'mp4',
)
MOVIE_REGEX = re.compile('.*\.(%s)$' % '|'.join(MOVIE_EXTENSIONS))


class Directory:

    def __init__(self, path):
        self.path = path
        self.directories = {}
        self.files = set()

    def add_file(self, name):
        self.files.add(name)

    def add_nested_directories(self, names):
        '''Create and add a nested directory for each name

        Return the directory nested most deeply

        '''
        if not names:
            return self
        new_path = names[0]
        try:
            directory = self.directories[new_path]
        except KeyError:
            directory = Directory(path.join(self.path, new_path))
            self.directories[new_path] = directory
        return directory.add_nested_directories(names[1:])


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


with open('templates/header.html') as header_file:
    header_template = header_file.read()

with open('templates/piece.html') as piece_file:
    piece_template = piece_file.read()

with open('templates/footer.html') as footer_file:
    footer = footer_file.read()


def process_directory(directory):

    directory_path = directory.path

    set_name = path.basename(directory_path)
    header = header_template % {
        'set_name': set_name,
    }
    content = ''

    for base_sub_dir, sub_dir in sorted(directory.directories.items()):
        if len(sub_dir.files) == 1:
            base_file_path = sub_dir.files.pop()
            base_name, _ = path.splitext(base_file_path)
            movie_path = path.join(base_sub_dir, base_file_path)
            name, _ = path.splitext(movie_path)
            subtitle_path = get_subtitle_path(directory_path, name)
            thumbnail_path = './%s/thumbnails/%s.jpg' % (base_sub_dir, base_name)
        else:
            movie_path = base_sub_dir
            subtitle_path = ''
            thumbnail_path = ''
        content += piece_template % {
            'movie_name': base_sub_dir,
            'movie_path': './%s' % movie_path,
            'subtitle_path': subtitle_path,
            'thumbnail_path': thumbnail_path,
        }

    for file_path in sorted(directory.files):

        movie_name = '%s, %s' % (set_name, file_path)
        name, _ = path.splitext(file_path)

        content += piece_template % {
            'movie_name': movie_name,
            'movie_path': './%s' % file_path,
            'subtitle_path': get_subtitle_path(directory_path, name),
            'thumbnail_path': './thumbnails/%s.jpg' % name,
        }

    with open(path.join(directory_path, INDEX_BASE), 'w') as index_file:
        index_file.write(header)
        index_file.write(content)
        index_file.write(footer)

    for sub_dir in directory.directories.values():
        process_directory(sub_dir)


root_directory = Directory('.')

for root, dirs, files in walk('files', followlinks=True):
    for name in files:
        if MOVIE_REGEX.match(name):
            parts = path_split(root)
            parent_directory = root_directory.add_nested_directories(parts)
            parent_directory.add_file(name)

process_directory(root_directory)
