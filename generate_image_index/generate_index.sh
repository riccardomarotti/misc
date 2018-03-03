#!/usr/bin/sh

#echo "${1}"
cd "${1}"
ls -1 | parallel generate_index.py
