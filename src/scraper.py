#!/usr/bin/env python3
# coding: utf-8


# IMPORTS -------------------------------------------------------------------+
# +--- Scraping imports -----------------------------------------------------+
import requests
from bs4 import BeautifulSoup
from src.image import Downloader


# +--- Decorator imports ----------------------------------------------------+
from functools import cached_property


# +--- Os imports -----------------------------------------------------------+
import os


# +--- Csv import -----------------------------------------------------------+
import csv


# +--- Urllib import --------------------------------------------------------+
import urllib.parse


# CLASSES -------------------------------------------------------------------+
# +--- BeautifulSoup4 generic HTML page scraper -----------------------------+
class Scraper:
    """ Base class to get a BeautifulSoup object from an URL. """
    def __init__(self, url: str):
        """ Scraper object constructor.
        Needs following argument :
        url - URL from the page to scrape. """
        self.url = url
        self.soup = BeautifulSoup(requests.get(self.url).content, features="html.parser")


# +--- books.toscrape.com generic scraper class -----------------------------+
class BooksToScrapeScraper(Scraper):
    """ Base class inherited from Scraper to scrape "books.toscrape.com" site.

    Class attributes :
    columns_name - contains the name of the columns for the CSV that will be generated later
    url_root - contains the root URL from the website
    """
    columns_name = (
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
    url_root = "https://books.toscrape.com/"

    @staticmethod
    def write_csv(file_path: str, *books_informations: list) -> None:
        """ Write a CSV file with class attribute "columns_name" as fields and
        given "book_informations" as lines. """
        with open(file_path, "w", encoding="utf-8", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=BooksToScrapeScraper.columns_name)
            writer.writeheader()
            writer.writerows(books_informations)


# +--- Product Scraper class ------------------------------------------------+
class ProductScraper(BooksToScrapeScraper):
    """ Class to scrape products pages from books.toscrape.com website.

    Privates properties _extracted_* are used to extract raw data from product
    soup. If an information can't be found in the soup, then an "Unknown" str
    object is returned.

    Public properties are used to return transformed data. Each CSV field has
    a property bearing its name.
    All informations can be obtained by calling "informations" property which
    will return a dict with fields name as keys and transformed data as
    values. """
    # extraction private properties
    @cached_property
    def _extracted_product_informations_from_table(self) -> dict:
        """ Return several product raw informations extracted from product
        page soup as str objects in a dict with following keys :
        "UPC" for universal_product_code field,
        "Price (incl. tax)" for price_including_tax field,
        "Price (excl. tax)" for price_excluding_tax field,
        "Availability" for number_available field. """
        informations = {
            "UPC": "Unknown",
            "Price (incl. tax)": "Unknown",
            "Price (excl. tax)": "Unknown",
            "Availability": "Unknown"
        }
        try:
            th_tags = self.soup.find("table", class_="table table-striped").find_all("th")
            return {th.string: th.find_next("td").string for th in th_tags if th.string in informations}
        except (AttributeError, IndexError) as error:
            return informations

    @cached_property
    def _extracted_title(self) -> str:
        """ Return title extracted from product page soup, in a str. """
        try:
            return self.soup.find("h1").string
        except AttributeError:
            return "Unknown"

    @cached_property
    def _extracted_product_description(self) -> str:
        """ Return description extracted from product page soup, in a str. """
        try:
            return self.soup.find("div", id="product_description").find_next("p").string
        except (AttributeError, IndexError) as error:
            return "Unknown"

    @cached_property
    def _extracted_category(self) -> str:
        """ Return category extracted from product page soup, in a str. """
        try:
            return self.soup.find("ul", class_="breadcrumb").find_all("a")[-1].string
        except (AttributeError, IndexError) as error:
            return "Unknown"

    @cached_property
    def _extracted_review_rating(self) -> str:
        """ Return review rating extracted from product page soup, in a str.
        """
        try:
            return self.soup.find("p", class_="star-rating")["class"][1]
        except IndexError:
            return "Unknown"

    @cached_property
    def _extracted_image_url(self) -> str:
        """ Return image URL extracted from product page soup, in a str. """
        try:
            return self.soup.find("div", class_="item active").find("img")["src"]
        except (AttributeError, IndexError) as error:
            return "Unknown"

    # transform public properties
    @cached_property
    def universal_product_code(self) -> str:
        """ Return universal product code in a str. """
        return self._extracted_product_informations_from_table["UPC"]

    @cached_property
    def title(self) -> str:
        """ Return title in a str. """
        return self._extracted_title

    @cached_property
    def price_including_tax(self) -> str:
        """ Return price including tax in a str. """
        return self._extracted_product_informations_from_table["Price (incl. tax)"].replace("£", "")

    @cached_property
    def price_excluding_tax(self) -> str:
        """ Return price excluding tax in a str. """
        return self._extracted_product_informations_from_table["Price (excl. tax)"].replace("£", "")

    @cached_property
    def number_available(self) -> str:
        """ Return availability title in a str. """
        return self._extracted_product_informations_from_table["Availability"].replace("In stock (", "").replace(" available)", "")

    @cached_property
    def product_description(self) -> str:
        """ Return description title in a str. """
        return self._extracted_product_description

    @cached_property
    def category(self) -> str:
        """ Return category in a str. """
        return self._extracted_category

    @cached_property
    def review_rating(self) -> str:
        """ Return review rating in a str. """
        return {
            "One": "1",
            "Two": "2",
            "Three": "3",
            "Four": "4",
            "Five": "5"
        }[self._extracted_review_rating]

    @cached_property
    def image_url(self) -> str:
        """ Return image URL in a str. """
        return urllib.parse.urljoin(self.url_root, self._extracted_image_url)

    # extracted and transformed informations merging
    @cached_property
    def informations(self) -> dict:
        """ Return all product transformed informations in a dict. """
        informations = {
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
        print(f"Successfully scraped <{self.title}> book informations from <{self.category}> category.")
        return informations

    # utils methods and properties
    @cached_property
    def clean_title(self):
        """ Return title cleaned from forbidden characters in path name. """
        title = ""
        for char in self.title:
            if not(char in "\\/\":*?<>|"):
                title += char
        return title


# +--- Category page URLs Scraper class -------------------------------------+
class CategoryPageURLScraper(Scraper):
    """ Class to scrape books URLs from one category page. """
    @cached_property
    def books_urls(self) -> list:
        """ Return all books URLs found on the page soup. """
        return [urllib.parse.urljoin(self.url, article.find("a")["href"]) for article in self.soup.find_all("article")]


# +--- Category Scraper class ------------------------------------------------+
class CategoryScraper(BooksToScrapeScraper):
    """ Class to scrape all books name and URL from a category. """
    def __init__(self, url: str, category_name: str, directory_path: str):
        """ CategoryScraper class constructor.

        Needs following arguments :
        url - URL from the category 1st page,
        category_name - name from the category to scrape,
        directory_path - path from the directory where CSV files will be generated. """
        url = url.replace("index.html", "")
        super(CategoryScraper, self).__init__(url)
        self.name = category_name
        self.directory = directory_path
        self._load()

    @cached_property
    def _page_number(self) -> int:
        """ Return the number of pages for this category. """
        pager = self.soup.find("ul", class_="pager")
        if pager:
            return int(pager.find("li", class_="current").string.split()[3])
        else:
            return 1

    @cached_property
    def _books_urls(self) -> list:
        """ Return the whole list of books URLs from this category. """
        # issue #25, error 404 with "*/page-1.html" url for 1-paged categories
        books_url_list = CategoryPageURLScraper(self.url).books_urls
        for page in range(2, self._page_number + 1):
            books_url_list += CategoryPageURLScraper(urllib.parse.urljoin(self.url, f"page-{page}.html")).books_urls
        return books_url_list

    @property   # no more cached (so that generator can be called 2 times)
    def books_scrapers(self) -> list:
        """ Return a generator of ProductScraper objects for all the books
        from this category. """
        # changed implementation so that all verbose doesn't freeze and print
        # every books scraped at the end of list comprehension.
        for url in self._books_urls:
            yield ProductScraper(url)

    def _load(self) -> None:
        """ Implement loading part from ETL process, doing following actions :
        Create a directory - is named as the category name..
        Create a subdirectory called "images" - contains images from all books
        of the category.
        Create a CSV file inside the category directory.
        Create the images in the subdirectory. """

        # urls scraping and verbose
        print(f"Scraping books URLs from the <{self.name}> category.")
        books_nb = len(self._books_urls)
        print(f"{books_nb} books found in <{self.name}> category.\n")

        # books scraping and verbose
        print(f"Scraping books informations from the <{self.name}> category.")

        # _load execution
        self.directory = os.path.join(self.directory, self.name)
        self.images_directory = os.path.join(self.directory, "images")
        try:
            os.mkdir(self.directory)
        except FileExistsError:
            pass
        try:
            os.mkdir(self.images_directory)
        except FileExistsError:
            pass
        self._write_csv()
        print(f"\nSuccessfully generated <{self.name}> category CSV file.\n")

        counter = 1
        for book in self.books_scrapers:
            print(f"({counter}/{books_nb})Downloading <{book.title}> image.")
            Downloader(book.image_url, book.clean_title + ".jpg", self.images_directory)
            print(f"Successfully scraped <{book.title}> image.")
            counter += 1

    def _write_csv(self) -> None:
        """ Create the CSV file containing all informations from the books
        from this category. """
        file_path = os.path.join(self.directory, self.name + ".csv")
        BooksToScrapeScraper.write_csv(file_path, *[book.informations for book in self.books_scrapers])


# +--- Website Scraper class -------------------------------------------------+
class WebsiteScraper(BooksToScrapeScraper):
    """ Class to scrape informations from all products on books.toscrape.com
    website. """
    def __init__(self, directory_path: str):
        """ Website Scraper class constructor.

        Automatically calls the _scrape private method to scrape the website.

        Needs following argument :
        directory_path - path from the directory where scraping results will
        be written. """
        super(WebsiteScraper, self).__init__("https://books.toscrape.com/")
        if os.path.exists(directory_path):
            self.directory = directory_path
        else:
            raise FileExistsError
        self._scrape()

    @cached_property
    def _categories(self) -> dict:
        """ Return the whole categories names and URLs as key and value in a
        dict. """
        return {" ".join(a.string.split()): self.url + a["href"] for a in self.soup.find("ul", class_="nav nav-list").find("ul").find_all("a")}

    def _scrape(self) -> None:
        """ Create a CategoryScraper for each found category. """
        # verbose
        print("Scraping categories")
        categories_nb = len(self._categories)
        print(f"{categories_nb} categories found.\n")
        counter = 1
        # method execution
        for name, url in self._categories.items():
            print(f"[{counter}/{categories_nb}] Scraping <{name}> category.")
            CategoryScraper(url, name, self.directory)
            print(f"Successfully scraped <{name}> category.\n\n")
            counter += 1
