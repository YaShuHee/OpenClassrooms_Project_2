#!/usr/bin/env python3
# coding: utf-8


from scraper import *


def main():
    url = input("Copy and paste a product page URL from the website https://books.toscrape.com:\n")
    product_informations = extract_product_informations(url)
    print("Extracted informations:\n=======================\n")
    for key, value in product_informations.items():
        print(f"{key}:\n{'-'*(len(key)+1)}\n{value}\n")


if __name__ == '__main__':
    main()
