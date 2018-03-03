#!/usr/bin/sh

cd "${1}"
ls -1 | parallel generate_index.py
