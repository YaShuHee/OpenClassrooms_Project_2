#!/usr/bin/env python3
# coding: utf-8


# IMPORTS -------------------------------------------------------------------+
# +--- Scraping imports -----------------------------------------------------+
import requests
import mimetypes


# +--- Os imports -----------------------------------------------------------+
import os


# CLASS ---------------------------------------------------------------------+
class Downloader:
    def __init__(self, url: str, image_name: str, directory_path: str):
        response = requests.get(url)
        extension = mimetypes.guess_extension(response.headers["content-type"])
        if os.path.exists(directory_path):
            self.path = os.path.join(directory_path, image_name + extension)
        if response.ok:
            self.content = response.content
            self._write()
        else:
            print(f"Couldn't download image at URL : {url}")
            del self

    def _write(self):
        with open(self.path, "wb") as file:
            file.write(self.content)
