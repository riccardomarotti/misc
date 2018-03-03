#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys


template = '''
<!DOCTYPE html>
<html>
  <head>
    <meta content="text/html;charset=utf-8" http-equiv="Content-Type">
    <meta content="utf-8" http-equiv="encoding">

    <script type="text/javascript">
        {{{PAGES_ARRAY}}}

        function load_image() {
            var page_index = window.location.search.split("=").slice(-1).pop()
            page_index = page_index ? page_index : 0

            var next_index = Math.min(pages.length-1, parseInt(page_index) + 1)
            var previous_index = Math.max(page_index - 1, 0)
            var page_file_name = pages[page_index]
            var image = document.getElementById("main_image");

            image.src = page_file_name;
            image.onload = function() {
                var is_touch_device = 'ontouchstart' in window;
                if(!(is_touch_device)){
                    set_links(image, previous_index, next_index);
                }

                set_swipe_events(image, previous_index, next_index)
            }
        }

        function set_swipe_events(image, previous_index, next_index) {
            var startX = null;
            var startY = null;

            document.addEventListener('touchstart',
                function(event) {
                    if(event.touches.length > 1) {
                        startX = null;
                        starrY = null;
                        return;
                    }

                    startX = event.touches[0].clientX;
                    startY = event.touches[0].clientY;
                }, false);

            document.addEventListener('touchmove',
                function(event){
                    var image_zoomed = event.view.visualViewport.scale > 1;
                    if(event.touches.length > 1 || startX === null || startY === null || image_zoomed) {
                        return;
                    }

                    var currentX = event.touches[0].clientX;
                    var currentY = event.touches[0].clientY;
                    var treshold = 10;

                    var deltaX = startX - currentX;
                    var deltaY = startY - currentY;

                    var isHorizontalSwipe = Math.abs(deltaX) > Math.abs(deltaY)

                    if(isHorizontalSwipe) {
                        if(deltaX > treshold) {
                            window.location.href = `?=${next_index}`
                        }
                        if(deltaX < -treshold) {
                            window.location.href = `?=${previous_index}`
                        }
                    }


                }, false);
        }

        function set_links(image, previous_index, next_index) {
            var image_width = image.clientWidth
            var image_height = image.clientHeight

            var image_map = document.getElementById("main_image_map");
            image_map.innerHTML = `<area shape="rect" coords="0, 0, ${image_width/2}, ${image_height}" href="?=${previous_index}" alt="Previous Page">`
            image_map.innerHTML += `<area shape="rect" coords="${image_width/2}, 0, ${image_width}, ${image_height}" href="?=${next_index}" alt="Next Page">`
        }


    </script>
  </head>

  <body onload="load_image()">
    <img id="main_image" style="width:100%;" usemap="#main_image_map" />
    <map id="main_image_map" name="main_image_map"></map>
  </body>
</html>
'''

if len(sys.argv) == 2:
    output_directory = sys.argv[1];
elif len(sys.argv) == 1:
    output_directory = sys.stdin.readlines()[0].strip()
else:
    print("Pass me the path containing your images, or pipe me that through stdin.")
    exit(1)

if not os.path.isdir(output_directory):
    print("{} does not seem to be a directory.".format(output_directory))
    exit(2)


output_file_name = os.path.join(output_directory, "./index.html")

if os.path.isfile(output_file_name):
    print("{} already exists.".format(output_file_name))
    exit(0)

files = os.listdir(output_directory)
javascript_pages_array = "pages = [" + ",".join(sorted(map(lambda file_name: '"{}"'.format(file_name), files))) + "];"

output = template.replace("{{{PAGES_ARRAY}}}", javascript_pages_array)

with open(output_file_name, 'w') as output_file:
    output_file.write(output)


print("File {} was correctly created.".format(output_file_name))
