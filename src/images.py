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
    """ An image downloader.
    Download binary data from an given url and write it in a file with given
    name at a given directory path.
    Instantiating an object from this class will automatically create a file
    without needing another method call.
    Even if designed to download image, it could be used to download any
    binary file from an url. """

    def __init__(self, url: str, image_name: str, directory_path: str):
        """ Downloader class constructor. It will automatically call private
        method _write. """
        response = requests.get(url)
        extension = mimetypes.guess_extension(response.headers["content-type"])
        if os.path.exists(directory_path):
            self.path = os.path.join(directory_path, image_name + extension)
        else:
            raise FileExistsError
        if response.ok:
            self.content = response.content
            self._write()
        else:
            print(f"Couldn't download image at URL : {url}")

    def _write(self):
        """ Write the downloaded binary data in a file. """
        with open(self.path, "wb") as file:
            file.write(self.content)
