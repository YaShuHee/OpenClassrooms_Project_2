#!/usr/bin/env python3
# coding: utf-8


# IMPORTS -------------------------------------------------------------------+
# +--- Scraping imports -----------------------------------------------------+
from scraper import *


# +--- OS imports -----------------------------------------------------------+
from os import sep


# FUNCTIONS -----------------------------------------------------------------+
def main():
    url = input("Copy and paste a product page URL from the website https://books.toscrape.com:\n")

    # extracted data
    extracted_informations = extract_product_informations(url)
    print("\nExtracted informations:\n=======================\n")
    for key, value in extracted_informations.items():
        print(f"{key} :  {value}\n{'-'*(len(key)+2)}\n")

    # transformed data
    transformed_informations = transform_product_informations(extracted_informations)
    print("\n\nTransformed informations:\n=========================\n")
    for key, value in transformed_informations.items():
        print(f"{key} :  {value}\n{'-'*(len(key)+2)}\n")

    # loaded data
    csv_content = generate_product_informations_csv(transformed_informations)
    # asking to user if they want to generate the csv
    answer = ""
    while answer != "y" and answer != "n":
        answer = input("Generate a CSV file for the extracted data ? (y/n) ").lower()
    if answer == "y":
        # asking to user where they want the file to be created
        directory = input("Copy and paste the directory where you want to create the CSV :")
        filename = input("Chose the file name :")
        file_path = directory + sep + filename
        answer = ""
        while answer != "y" and answer != "n":
            answer = input(f"Confirm creation of the file {file_path}? (y/n) ").lower()
        if answer == "y":
            write_csv(file_path, csv_content)


# CODE EXECUTION ------------------------------------------------------------+
if __name__ == '__main__':
    main()
