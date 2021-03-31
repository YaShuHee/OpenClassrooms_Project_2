#!/usr/bin/env python3
# coding: utf-8


# IMPORTS -------------------------------------------------------------------+
# +--- Scraping imports -----------------------------------------------------+
from scraper import WebsiteScraper


# FUNCTIONS -----------------------------------------------------------------+
def main():
    # asking to user where they want the files to be created
    directory = input("Copy and paste the directory path where you want to create the CSV files :\n")
    answer = ""
    while answer != "y" and answer != "n":
        answer = input(f"Scraping may take several minutes. Confirm CSV creation at <{directory}> path ? (y/n) ").lower()
    if answer == "y":
        WebsiteScraper(directory)


# CODE EXECUTION ------------------------------------------------------------+
if __name__ == '__main__':
    main()
