import sys
import getopt
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup


def main(cookie):
    cookies = {'DelosID': cookie}

    for n in range(1, 208):
        html = get(
            f'https://www.fantascienza.com/delos/{n}', cookies=cookies).content
        links = BeautifulSoup(html, 'html.parser').findAll(
            "div", {"class": "download-version"})
        for l in links:
            delosEpubLink = l.select("a")[0]['href']
            delosEbub = get(delosEpubLink)

            filename = f"./delos-{n:03d}.zip"
            print(f"creating {filename}...")
            with open(filename, 'wb') as f:
                f.write(delosEbub.content)


if __name__ == "__main__":
    main(sys.argv[1])
