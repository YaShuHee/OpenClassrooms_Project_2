#!/usr/bin/env python3
# coding: utf-8


# IMPORTS -------------------------------------------------------------------+
# +--- Scraping imports -----------------------------------------------------+
from scraper import *


# FUNCTIONS -----------------------------------------------------------------+
def main():
    url = input("Copy and paste a product page URL from the website https://books.toscrape.com:\n")

    # ProductScraper object initialisation
    product_scraper = ProductScraper(url)

    # asking to user if they want to generate the csv
    answer = ""
    while answer != "y" and answer != "n":
        answer = input("Generate a CSV file for the extracted data ? (y/n) ").lower()
    if answer == "y":
        # asking to user where they want the file to be created
        directory = input("Copy and paste the directory where you want to create the CSV :")
        filename = input("Chose the file name :")
        answer = ""
        while answer != "y" and answer != "n":
            answer = input(f"Confirm creation of the file \"{filename}\" ? (y/n) ").lower()
        if answer == "y":
            product_scraper.write_csv(directory, filename)


# CODE EXECUTION ------------------------------------------------------------+
if __name__ == '__main__':
    main()
