import re
import csv

import requests
from bs4 import BeautifulSoup



def rating_in_letter_to_interger(rating_in_letter):
    """Transform rating in srting to rating in interger

    Args:
        rating_in_letter (str): Should be either; "Zero", "One", "Two", "Three", "Four" or "Five" 

    Returns:
        int
    """
    numbers = {"Zero": 0, "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    rating_int = numbers[rating_in_letter]
    return rating_int



def get_data_from_product_page(product_page_url, category):
    """Scrap data from a product page

    Args:
        product_page_url (str)
        category (str): category of the scrapped book

    Returns:
        list: [product_page_url, upc, title, price_including_tax, price_excluding_tax, number_available, description, category, review_rating, image_url]
    """
    page = requests.get(product_page_url)
    soup = BeautifulSoup(page.content, "html.parser")
    if page.ok:
        data_table = []

        table = soup.find("table", "table table-striped")
        rows = table.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            for item in cols:
                item = item.text
                data_table.append(item)
        upc = data_table[0]
        price_including_tax = data_table[2]
        price_excluding_tax = data_table[3]
        extracted_number = re.findall(
            r"\d+", data_table[5]# Searching for one or more digit in data_table[5] = "In stock (20 available)"" for example
        )  
        number_available = extracted_number[0]
        title = soup.find("li", class_="active").text
        on_top_of_description = soup.find("div", class_="sub-header")
        description = on_top_of_description.find_next("p").text
        image_soup = soup.find("div", class_="item active").img
        image_path = image_soup["src"]
        image_url = (
            "http://books.toscrape.com" + image_path[5:]  # Removing ../.. at the begining of the path
        )
        review_rating_tag = soup.find(
            "p", "star-rating"
        ).attrs  # This return {'class': ['star-rating', 'review_rating_letter']} hence the following:
        review_rating_letter = review_rating_tag["class"][1]
        review_rating = rating_in_letter_to_interger(review_rating_letter)
        product_data = [
            product_page_url.strip(), 
            upc.strip(),
            title.strip(),
            price_including_tax.strip(),
            price_excluding_tax.strip(),
            number_available.strip(),
            description.strip(), 
            category.strip(),
            review_rating,
            image_url.strip(),
        ]
        return product_data



def get_all_categories(index):
    """Scrap and return all category from the index

    Args:
        index (str): In reality only "https://books.toscrape.com/"

    Returns:
        list
    """
    page = requests.get(index)
    categories = []
    if page.ok:
        soup = BeautifulSoup(page.content, "html.parser")
        links_containing_category = soup.find_all("a", href=re.compile("category"))
        for links in links_containing_category:
            full_path = links["href"]
            only_the_category = full_path[25:][:-11]
            categories.append(only_the_category)
        del categories[0] # compensate for index
    return categories



def get_catalogue_urls_from_a_category(category):
    """Return all catalogue page's url for a given category

    Args:
        category (str)

    Returns:
        list:  a list of url (can be only one) of the pages for the category
    """
    urls = []
    url_index = (
        "http://books.toscrape.com/catalogue/category/books/" + category + "/index.html"
    )
    urls.append(url_index)
    i = 2
    while True:
        url_pages = (
            "http://books.toscrape.com/catalogue/category/books/"
            + category
            + "/page-"
            + str(i)
            + ".html"
        )
        page = requests.get(url_pages)
        if page.ok:
            urls.append(url_pages)
            i += 1
        else:
            break
    return urls


def get_page_product_url(catalogue_url):
    """Scraps urls of procuct pages from a catalog page

    Args:
        catalogue_url (str): url of a catalogue page

    Returns:
        list: a list of product page urls
    """
    product_page_urls = []
    page = requests.get(catalogue_url)
    if page.ok:
        soup = BeautifulSoup(page.content, "html.parser")
        h3 = soup.find_all("h3")
        for titre in h3:
            path = titre.a["href"][8:]
            url = "https://books.toscrape.com/catalogue" + path
            product_page_urls.append(url)
    return product_page_urls
