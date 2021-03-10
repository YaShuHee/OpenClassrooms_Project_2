#!/usr/bin/env python3
# coding: utf-8


from scraper import *


def main():
    url = input("Copy and paste a product page URL from the website https://books.toscrape.com:\n")

    # extracted value
    extracted_informations = extract_product_informations(url)
    print("\nExtracted informations:\n=======================\n")
    for key, value in extracted_informations.items():
        print(f"{key} :  {value}\n{'-'*(len(key)+2)}\n")

    # transformed value
    transformed_informations = transform_product_informations(extracted_informations)
    print("\n\nTransformed informations:\n=========================\n")
    for key, value in transformed_informations.items():
        print(f"{key} :  {value}\n{'-'*(len(key)+2)}\n")


if __name__ == '__main__':
    main()
