#!/usr/bin/env python3
# coding: utf-8


import requests
import bs4
from bs4 import BeautifulSoup


# BEAUTIFULSOUP MANIPULATION FUNCTIONS ---------------------------------------
def get_soup(url: str) -> BeautifulSoup:
    """ Send a GET request to the given URL, parse the returned HTML
    and return a BeautifulSoup object, which can be used to scrape data. """
    return BeautifulSoup(requests.get(url).content, "html.parser")


# EXTRACTION FUNCTIONS -------------------------------------------------------
def extract_product_informations(url: str) -> dict:
    """ Extract all the product informations from its soup. """
    soup = get_soup(url)
    return {
        "product_page_url": url,
        **extract_product_title(soup),
        **extract_product_category(soup),
        **extract_product_review_rating(soup),
        **extract_product_description(soup),
        **extract_product_infos_from_table(soup)
    }


def extract_product_title(soup: BeautifulSoup) -> dict:
    """ Extract the product title from its soup. """
    return {"title": soup.find("h1").string}


def extract_product_category(soup: BeautifulSoup) -> dict:
    """ Extract the product category from its soup. """
    return {"category": soup.find("ul", class_="breadcrumb").find_all("a")[-1].string}


def extract_product_review_rating(soup: BeautifulSoup) -> dict:
    """ Extract the product review rating from its soup. """
    return {"review_rating": soup.find("p", class_="star-rating")["class"][1]}


def extract_product_description(soup: BeautifulSoup) -> dict:
    """ Extract the product description from its soup. """
    return {"product_description": soup.find("div", id="product_description").find_next("p").string}


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


# TRANSFORMATION FUNCTIONS ---------------------------------------------------
def transform_product_informations(extracted_infos: dict) -> dict:
    """ Transform all the previously extracted product informations. """
    pass


def transform_product_review_rating(review_rating) -> str:
    """ Format the product review rating. """
    pass


def transform_product_description(description: str) -> str:
    """ Format the product description. """
    pass


def transform_product_infos_from_table(table_infos: dict) -> str:
    """ Transform the following product informations, previously extracted :
            - price_including_tax,
            - price_excluding_tax,
            - number_available. """
    pass


def transform_product_prices(price: str) -> str:
    """ Format the product prices. """
    pass


def transform_product_availability(availabilty: str) -> str:
    """ Format the product availability. """
    pass


# LOADING FUNCTIONS ----------------------------------------------------------
def generate_product_informations_csv(transformed_infos: dict) -> dict:
    """ Generate and write the product CSV. """
    pass
