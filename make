#!/bin/bash

set -e


cd "$(dirname "$0")"

cat header.html > index.html

while read -d $'\0' file
do

    dir="$(basename "$(dirname "$file")")"
    thumbnail="${file}.jpg"
    subtitle="${file}-vi.srt"

    cat <<EOH >> index.html
<li class='span4'>
    <div class='thumbnail'>
        <a href="$file">
            <img src="$thumbnail" alt='' width='600'/>
        </a>
        <h3><a href="$file">$dir</a></h3>
        <a href="$subtitle">Phụ đề</a>
    </div>
</li>
EOH

done < <(find files/ -type f \
                     -regextype posix-extended \
                     -regex '.*\.(mkv|mp4|avi)' \
                     -print0 | sort -z)

cat footer.html >> index.html
