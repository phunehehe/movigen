#!/bin/bash

set -e


bin_dir="$(cd "$(dirname "$0")" && pwd)"
cd "$bin_dir"


cat header.html > index.html

while read -d $'\0' file
do

    dir="$(basename "$(dirname "$file")")"
    thumbnail="${file}.jpg"
    subtitle="${file}-vi.srt"

    [[ -f "$thumbnail" ]] || ffmpeg -itsoffset -120 -i "$file" -vframes 1 -s 600x400 "$thumbnail"

    echo "
<li class='span4'>
    <div class='thumbnail'>
        <a href='$file'>
            <img src='$file.jpg' alt='' width='600'/>
        </a>
        <h3><a href='$file'>"$dir"</a></h3>
        <a href='$subtitle'>Phụ đề</a>
    </div>
</li>
    " >> index.html

done < <(find files/ -type f -regextype posix-extended -regex '.*\.(mkv|mp4|avi)' -print0 | sort -z)

cat footer.html >> index.html
