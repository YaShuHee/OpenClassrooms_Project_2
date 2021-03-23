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
