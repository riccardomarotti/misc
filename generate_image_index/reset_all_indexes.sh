#!/usr/bin/sh

find . -iname "index\.html" | parallel rm
ls -1 -d */ | parallel ./generate_index.sh
