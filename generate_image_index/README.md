This is a trivial script that create an index file to navigate a list of images.

I use this for comics: when you have N images in a directory, and you serve it in a web server, you can easily create a simple index.

To do this, copy `generate_index.py` in your `PATH`, and be sure to make it executable.

Then

    cd YOUR_DIRECTORY_CONTAINING_IMAGES
    generate_index.py .

Or lets say you have a lot of direcotries containing images.

Then

     cd YOUR_DIRECTORY_CONTAINING_A_LOT_OF_DIRECTORIES
     ls -1 | parallel generate_index.py


Thanks to [GNU](https://www.gnu.org/) for [Parallel](https://www.gnu.org/software/parallel/).
