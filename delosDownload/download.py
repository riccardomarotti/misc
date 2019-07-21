import sys
import getopt
import re
from requests import get, head
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup


def main(cookie):
    cookies = {'DelosID': cookie}

    for n in range(1, 209):
        html = get(
            f'https://www.fantascienza.com/delos/{n}', cookies=cookies).content
        links = BeautifulSoup(html, 'html.parser').findAll(
            "div", {"class": "download-version"})
        for l in links:
            delosEpubLink = l.select("a")[0]['href']
            filename = re.findall("filename=\"(.+)\"", head(delosEpubLink).headers['content-disposition'])[0]
            delosEbub = get(delosEpubLink)

            print(f"creating {filename}...")
            with open(filename, 'wb') as f:
                f.write(delosEbub.content)


if __name__ == "__main__":
    main(sys.argv[1])
