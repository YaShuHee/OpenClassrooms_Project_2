#!/usr/bin/env python3
# coding: utf-8


# IMPORTS -------------------------------------------------------------------+
# +--- Scraping imports -----------------------------------------------------+
import requests
import bs4
from bs4 import BeautifulSoup
from images import Downloader


# +--- Decorator imports ----------------------------------------------------+
from functools import cached_property


# +--- Os imports -----------------------------------------------------------+
from os import sep, mkdir


# +--- Csv import -----------------------------------------------------------+
import csv


# CLASSES -------------------------------------------------------------------+
# +--- BeautifulSoup4 generic HTML page scraper -----------------------------+
class Scraper:
    def __init__(self, url: str):
        self.url = url
        self.soup = BeautifulSoup(requests.get(self.url).content, features="html.parser")


# +--- books.toscrape.com generic scraper class -----------------------------+
class BooksToScrapeScraper(Scraper):
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

    @staticmethod
    def write_csv(file_path: str, *books_informations: list) -> None:
        with open(file_path, "w", encoding="utf-8", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=BooksToScrapeScraper.columns_tuple)
            writer.writeheader()
            writer.writerows(books_informations)


# +--- Product Scraper class ------------------------------------------------+
class ProductScraper(BooksToScrapeScraper):
    # extraction private properties ------------------------------------------
    @cached_property
    def _extracted_product_informations_from_table(self) -> dict:
        informations = {
            "UPC": "Unknown",
            "Price (incl. tax)": " Unknown",
            "Price (excl. tax)": " Unknown",
            "Availability": "Unknown"
        }
        try:
            th_tags = self.soup.find("table", class_="table table-striped").find_all("th")
            return {th.string: th.find_next("td").string for th in th_tags if th.string in informations}
        except (AttributeError, IndexError) as error:
            return informations

    @cached_property
    def _extracted_universal_product_code(self) -> str:
        return self._extracted_product_informations_from_table["UPC"]
    
    @cached_property
    def _extracted_title(self) -> str:
        try:
            return self.soup.find("h1").string
        except AttributeError:
            return "Unknown"
    
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
        try:
            return self.soup.find("div", id="product_description").find_next("p").string
        except (AttributeError, IndexError) as error:
            return "Unknown"
    
    @cached_property
    def _extracted_category(self) -> str:
        try:
            return self.soup.find("ul", class_="breadcrumb").find_all("a")[-1].string
        except (AttributeError, IndexError) as error:
            return "Unknown"
    
    @cached_property
    def _extracted_review_rating(self) -> str:
        try:
            return self.soup.find("p", class_="star-rating")["class"][1]
        except IndexError:
            return "Unknown"
    
    @cached_property
    def _extracted_image_url(self) -> str:
        try:
            return self.soup.find("div", class_="item active").find("img")["src"]
        except (AttributeError, IndexError) as error:
            return "Unknown"

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
        return self._extracted_product_description
    
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
    def informations(self) -> dict:
        return {
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

    @cached_property
    def clean_title(self):
        title = ""
        for char in self.title:
            if not(char in "\\/\":*?<>|"):
                title += char
        return title


# +--- Category page URLs Scraper class -------------------------------------+
class CategoryPageURLScraper(Scraper):
    @cached_property
    def books_url_list(self) -> list:
        return [article.find("a")["href"].replace("../../..", "http://books.toscrape.com/catalogue") for article in self.soup.find_all("article")]


# +--- Category Scraper class ------------------------------------------------+
class CategoryScraper(BooksToScrapeScraper):
    def __init__(self, url: str, category_name: str, directory: str):
        url = url.replace("index.html", "")
        super(CategoryScraper, self).__init__(url)
        self.name = category_name
        self.directory = directory
        self._load()
    
    @cached_property
    def _page_number(self) -> int:
        pager = self.soup.find("ul", class_="pager")
        if pager:
            return int(pager.find("li", class_="current").string.split()[3])
        else:
            return 1

    @cached_property
    def _books_url_list(self) -> list:
        # issue #25, error 404 with "*/page-1.html" url for one page categories
        books_url_list = CategoryPageURLScraper(self.url).books_url_list
        for page in range(2, self._page_number + 1):
            books_url_list += CategoryPageURLScraper(f"{self.url}page-{page}.html").books_url_list
        return books_url_list

    @cached_property
    def books_scrapers(self):
        return [ProductScraper(url) for url in self._books_url_list]

    @cached_property
    def csv_informations_lines(self) -> list:
        return [book_scraper.csv_informations_line for book_scraper in self.books_scrapers]

    def _load(self):
        # create 'category directory'
        # create 'images subdirectory'
        # write the csv in 'category directory'
        # write the images in the 'image subdirectory'
        self.directory += sep + self.name
        self.images_directory = self.directory + sep + "images"
        mkdir(self.directory)
        mkdir(self.images_directory)
        self._write_csv()
        for book in self.books_scrapers:
            Downloader(book.image_url, book.clean_title + ".jpg", self.images_directory)

    def _write_csv_old(self):
        file_path = self.directory + sep + self.name + ".csv"
        BooksToScrapeScraper.write_csv(file_path, *self.csv_informations_lines)

    def _write_csv(self):
        file_path = self.directory + sep + self.name + ".csv"
        BooksToScrapeScraper.write_csv(file_path, *[book.informations for book in self.books_scrapers])


# +--- Website Scraper class -------------------------------------------------+
class WebsiteScraper(BooksToScrapeScraper):
    def __init__(self, directory):
        super(WebsiteScraper, self).__init__("https://books.toscrape.com/")
        self.directory = directory
        self._scrape()

    @cached_property
    def _categories(self) -> dict:
        return {" ".join(a.string.split()): self.url + a["href"] for a in self.soup.find("ul", class_="nav nav-list").find("ul").find_all("a")}

    def _scrape(self) -> None:
        for name, url in self._categories.items():
            CategoryScraper(url, name, self.directory)
