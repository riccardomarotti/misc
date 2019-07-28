import sys
import getopt
from contextlib import closing
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def main(linkToMainPage):
    driver = webdriver.Firefox()
    driver.get(linkToMainPage)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'listing')))
    html = driver.page_source

    links = BeautifulSoup(html, 'html.parser').findAll(
        "table", {"class": "listing"})[0].select('a')

    for l in links:
        print(l['href'])

    driver.close()


if __name__ == "__main__":
    if(len(sys.argv) != 2):
        print("You should give me the link of a page of a comic, such as 'https://readcomiconline.to/Comic/The-Boys'")
        exit()

    main(sys.argv[1])
