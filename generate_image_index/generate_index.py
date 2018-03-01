#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

if len(sys.argv) != 2:
    print("Pass me the path containing your images.")
    exit(0)

output_directory = sys.argv[1];
files = os.listdir(output_directory)
javascript_pages_array = "pages = [" + ",".join(sorted(map(lambda file_name: '"{}"'.format(file_name), files))) + "];"

with open("./index.html.template", 'r') as template_file:
    template = template_file.read()

output = template.replace("{{{PAGES_ARRAY}}}", javascript_pages_array)

with open(os.path.join(output_directory, "./index.html"), 'w') as output_file:
    output_file.write(output)

