#!/usr/bin/env python3
# coding: utf-8


# IMPORTS -------------------------------------------------------------------+
# +--- Scraping imports -----------------------------------------------------+
import requests


# +--- Os imports -----------------------------------------------------------+
from os import sep


# CLASS ---------------------------------------------------------------------+
class Downloader:
    def __init__(self, url: str, name: str, directory_path: str):
        self.url = url
        self.path = directory_path + sep + name
        response = requests.get(url)
        if response.ok:
            self.content = response.content
            self._write()
        else:
            print(f"Couldn't download image at URL : {url}")
            del self

    def _write(self):
        with open(self.path, "wb") as file:
            file.write(self.content)


# CODE EXECUTION ------------------------------------------------------------+
if __name__ == '__main__':
    Downloader("http://books.toscrape.com/media/cache/fe/72/fe72f0532301ec28892ae79a629a293c.jpg", "A light in the Attic.jpg", input("directory :"))
