#!/bin/bash

set -e


bin_dir="$(cd "$(dirname "$0")" && pwd)"
cd "$bin_dir"


cat header.html > index.html

for i in movies/*
do
    for f in "$i"/*.mkv
    do
        b="$(basename "$f")"
        echo "
<li class='span4'>
    <div class='thumbnail'>
        <a href='$f'>
            <img src='thumbnails/$b.jpg' alt='' width='600'/>
        </a>
        <h3><a href='$f'>$b</a></h3>
    </div>
</li>
        " >> index.html
    done
done

cat footer.html >> index.html
