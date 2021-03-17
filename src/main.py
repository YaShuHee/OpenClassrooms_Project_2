#!/usr/bin/env python3
# coding: utf-8


# IMPORTS -------------------------------------------------------------------+
# +--- Scraping imports -----------------------------------------------------+
from scraper import *


# FUNCTIONS -----------------------------------------------------------------+
def main():
    url = input("Copy and paste a category first page URL from the website https://books.toscrape.com:\n")
    category_name = input("Category name (will be your filename):\n")

    # CategoryScraper object initialisation
    category_scraper = CategoryScraper(url, category_name)

    # asking to user where they want the file to be created
    directory = input("Copy and paste the directory where you want to create the CSV :\n")
    filename = category_name + ".csv"
    answer = ""
    while answer != "y" and answer != "n":
        answer = input(f"Scraping may take several minutes. Confirm creation of the file \"{filename}\" ? (y/n) ").lower()
    if answer == "y":
        category_scraper.write_csv(directory)


# CODE EXECUTION ------------------------------------------------------------+
if __name__ == '__main__':
    main()
