#!/usr/bin/env python3
# coding: utf-8


import requests
import bs4
from bs4 import BeautifulSoup


# BEAUTIFULSOUP MANIPULATION FUNCTIONS ---------------------------------------
def get_soup(url: str) -> BeautifulSoup:
    """ Parse an URL and return a BeautifulSoup object. """
    pass


# EXTRACTION FUNCTIONS -------------------------------------------------------
def extract_product_informations(soup: BeautifulSoup) -> dict:
    """ Extract all the product informations from its soup. """
    pass


def extract_product_title(soup: BeautifulSoup) -> dict:
    """ Extract the product title from its soup. """
    pass


def extract_product_category(soup: BeautifulSoup) -> dict:
    """ Extract the product category from its soup. """
    pass


def extract_product_review_rating(soup: BeautifulSoup) -> dict:
    """ Extract the product review rating from its soup. """
    pass


def extract_product_description(soup: BeautifulSoup) -> dict:
    """ Extract the product description from its soup. """
    pass


def extract_product_infos_from_table(soup: BeautifulSoup) -> dict:
    """ Extract several product informations from a table in its soup :
            - universal_product_code,
            - price_including_tax,
            - price_excluding_tax,
            - number_available. """
    pass


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
