#!/usr/bin/env python3
# coding: utf-8


# IMPORTS -------------------------------------------------------------------+
# +--- Scraping imports -----------------------------------------------------+
import requests
import bs4
from bs4 import BeautifulSoup


# +--- Decorator imports ----------------------------------------------------+
from functools import cache


# FUNCTIONS -----------------------------------------------------------------+
# +--- BeautifulSoup4 manipulations functions -------------------------------+
def get_soup(url: str) -> BeautifulSoup:
    """ Send a GET request to the given URL, parse the returned HTML
    and return a BeautifulSoup object, which can be used to scrape data. """
    return BeautifulSoup(requests.get(url).content, "html.parser")


# +--- Extraction functions -------------------------------------------------+
def extract_product_informations(url: str) -> dict:
    """ Extract all the product informations from its soup. """
    soup = get_soup(url)
    return {
        "product_page_url": url,
        **extract_product_title(soup),
        **extract_product_description(soup),
        **extract_product_category(soup),
        **extract_product_review_rating(soup),
        **extract_product_image_url(soup),
        **extract_product_infos_from_table(soup),
    }


def extract_product_title(soup: BeautifulSoup) -> dict:
    """ Extract the product title from its soup. """
    return {"title": soup.find("h1").string}


def extract_product_description(soup: BeautifulSoup) -> dict:
    """ Extract the product description from its soup. """
    return {"product_description": soup.find("div", id="product_description").find_next("p").string}


def extract_product_category(soup: BeautifulSoup) -> dict:
    """ Extract the product category from its soup. """
    return {"category": soup.find("ul", class_="breadcrumb").find_all("a")[-1].string}


def extract_product_review_rating(soup: BeautifulSoup) -> dict:
    """ Extract the product review rating from its soup. """
    return {"review_rating": soup.find("p", class_="star-rating")["class"][1]}


def extract_product_image_url(soup: BeautifulSoup) -> dict:
    """ Extract the product image URL. """
    return {
        "image_url":
            soup.find("div", class_="item active").find("img")["src"]
    }


def extract_product_infos_from_table(soup: BeautifulSoup) -> dict:
    """ Extract several product informations from a table in its soup :
            - universal_product_code,
            - price_including_tax,
            - price_excluding_tax,
            - number_available. """
    headers_to_extract = ("UPC", "Price (excl. tax)", "Price (incl. tax)", "Availability")
    th_tags = soup.find("table", class_="table table-striped").find_all("th")
    infos = {th.string: th.find_next("td").string for th in th_tags if th.string in headers_to_extract}
    return infos


# +--- Transformation functions ---------------------------------------------+
def transform_product_informations(extracted_infos: dict) -> dict:
    """ Transform all the previously extracted product informations. """
    transformed_informations = {
        "product_page_url":
            extracted_infos["product_page_url"],
        "universal_product_code":
            extracted_infos["UPC"],
        "title":
            extracted_infos["title"],
        "price_including_tax":
            transform_product_prices(extracted_infos["Price (incl. tax)"]),
        "price_excluding_tax":
            transform_product_prices(extracted_infos["Price (excl. tax)"]),
        "number_available":
            transform_product_availability(extracted_infos["Availability"]),
        "product_description":
            transform_product_description(extracted_infos["product_description"]),
        "category":
            extracted_infos["category"],
        "review_rating":
            transform_product_review_rating(extracted_infos["review_rating"]),
        "image_url":
            transform_product_image_url(extracted_infos["image_url"]),
    }
    transformed_informations = {
        key: quote(value) for key, value in transformed_informations.items()
    }
    return transformed_informations


def quote(string: str) -> str:
    return f"\"{string}\""


def transform_product_prices(price: str) -> str:
    """ Format the product prices. """
    return price[1:]


def transform_product_availability(availabilty: str) -> str:
    """ Format the product availability. """
    return availabilty.replace("In stock (", "").replace(" available)", "")


def transform_product_description(description: str) -> str:
    """ Format the product description. """
    return description.replace("\"", "\"\"")


@cache  # will calculate only once for each argument
def transform_product_review_rating(review_rating: str) -> str:
    """ Format the product review rating. """
    return {
        "One": "1",
        "Two": "2",
        "Three": "3",
        "Four": "4",
        "Five": "5"
    }[review_rating]


def transform_product_image_url(url: str) -> str:
    return url.replace("../..", "https://books.toscrape.com")


# +--- Loading functions ----------------------------------------------------+
def generate_product_informations_csv(transformed_infos: dict) -> dict:
    """ Generate the product CSV content. """
    csv_content = ""
    to_write = ""
    for column in transformed_infos.keys():
        to_write += f"{column}, "
    csv_content += to_write[:-2] + "\n"
    to_write = ""
    for value in transformed_infos.values():
        to_write += f"{value}, "
    csv_content += to_write[:-2]
    return csv_content


def write_csv(file_path: str, csv_content: str) -> bool:
    """ Write the CSV. """
    with open(file_path, "w") as file:
        file.write(csv_content)
