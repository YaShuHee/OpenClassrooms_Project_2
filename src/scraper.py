#!/usr/bin/env python3
# coding: utf-8


# IMPORTS -------------------------------------------------------------------+
# +--- Scraping imports -----------------------------------------------------+
import requests
import bs4
from bs4 import BeautifulSoup


# +--- Decorator imports ----------------------------------------------------+
from functools import cached_property


# +--- Os imports -----------------------------------------------------------+
from os import sep


# CLASSES -------------------------------------------------------------------+
# +--- books.toscrape.com generic scraper class -----------------------------+
class Scraper:
    columns_tuple = (
            "product_page_url",
            "universal_product_code",
            "title",
            "price_including_tax",
            "price_excluding_tax",
            "number_available",
            "product_description",
            "category",
            "review_rating",
            "image_url"
            )
    csv_columns_line = ",".join(columns_tuple)

    def __init__(self, url: str):
        self.url = url
        self.soup = BeautifulSoup(requests.get(self.url).content, features="html.parser")

    @staticmethod
    def quote(string: str) -> str:
        return f"\"{string}\""

    def write_csv(self, file_path: str, *info_lines: list):
        with open(file_path, "w") as file:
            file.write("\n".join([Scraper.csv_columns_line, *info_lines]))


# +--- Product Scraper class ------------------------------------------------+
class ProductScraper(Scraper):
    def __init__(self, url: str):
        Scraper.__init__(self, url)

    # extraction private properties ------------------------------------------
    @cached_property
    def _extracted_product_informations_from_table(self) -> str:
        headers_to_extract = ("UPC", "Price (incl. tax)", "Price (excl. tax)", "Availability")
        th_tags = self.soup.find("table", class_="table table-striped").find_all("th")
        infos = {th.string: th.find_next("td").string for th in th_tags if th.string in headers_to_extract}
        return infos

    @cached_property
    def _extracted_universal_product_code(self) -> str:
        return self._extracted_product_informations_from_table["UPC"]
    
    @cached_property
    def _extracted_title(self) -> str:
        return self.soup.find("h1").string
    
    @cached_property
    def _extracted_price_including_tax(self) -> str:
        return self._extracted_product_informations_from_table["Price (incl. tax)"]
    
    @cached_property
    def _extracted_price_excluding_tax(self) -> str:
        return self._extracted_product_informations_from_table["Price (excl. tax)"]
    
    @cached_property
    def _extracted_number_available(self) -> str:
        return self._extracted_product_informations_from_table["Availability"]
    
    @cached_property
    def _extracted_product_description(self) -> str:
        return self.soup.find("div", id="product_description").find_next("p").string 
    
    @cached_property
    def _extracted_category(self) -> str:
        return self.soup.find("ul", class_="breadcrumb").find_all("a")[-1].string
    
    @cached_property
    def _extracted_review_rating(self) -> str:
        return self.soup.find("p", class_="star-rating")["class"][1]
    
    @cached_property
    def _extracted_image_url(self) -> str:
        return self.soup.find("div", class_="item active").find("img")["src"]

    # transform public properties --------------------------------------------
    @cached_property
    def universal_product_code(self) -> str:
        return self._extracted_universal_product_code
    
    @cached_property
    def title(self) -> str:
        return self._extracted_title
    
    @cached_property
    def price_including_tax(self) -> str:
        return self._extracted_price_including_tax[1:]
    
    @cached_property
    def price_excluding_tax(self) -> str:
        return self._extracted_price_excluding_tax[1:]
    
    @cached_property
    def number_available(self) -> str:
        return self._extracted_number_available.replace("In stock (", "").replace(" available)", "")
    
    @cached_property
    def product_description(self) -> str:
        return self._extracted_product_description.replace("\"", "\"\"")
    
    @cached_property
    def category(self) -> str:
        return self._extracted_category
    
    @cached_property
    def review_rating(self) -> str:
        return {
        "One": "1",
        "Two": "2",
        "Three": "3",
        "Four": "4",
        "Five": "5"
    }[self._extracted_review_rating]

    @cached_property
    def image_url(self) -> str:
        return self._extracted_image_url.replace("../..", "https://books.toscrape.com")

    # extracted and transformed informations merging -------------------------
    @cached_property
    def _informations_dict(self) -> dict:
        infos_dict = {
            "product_page_url": self.url,
            "universal_product_code": self.universal_product_code,
            "title": self.title,
            "price_including_tax": self.price_including_tax,
            "price_excluding_tax": self.price_excluding_tax,
            "number_available": self.number_available,
            "product_description": self.product_description,
            "category": self.category,
            "review_rating": self.review_rating,
            "image_url": self.image_url,
        }
        return {key: Scraper.quote(value) for key, value in infos_dict.items()}

    @cached_property
    def csv_informations_line(self) -> str:
        return ",".join(self._informations_dict.values())

    # load method ------------------------------------------------------------
    def write_csv(self, directory: str, file_name: str = ""):
        if file_name == "":
            file_name = self.title + ".csv"
        file_path = directory + sep + file_name
        super().write_csv(file_path, self.csv_informations_line)
