#!/usr/bin/sh

find . -iname "index\.html" | parallel rm
ls -1 | parallel ./generate_index.sh
