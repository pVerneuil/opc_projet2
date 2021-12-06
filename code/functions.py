import re
import csv

import requests
from bs4 import BeautifulSoup


# Transform rating in srting to rating in interger
def rating_in_letter_to_interger(rating_in_letter):
    numbers = {"Zero": 0, "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    rating_int = numbers[rating_in_letter]
    return rating_int


# Scrap thoose data from a product page:
#  product_page_url, upc, title, price_including_tax, price_excluding_tax, number_available, description, category, review_rating, image_url
def get_data_from_product_page(product_page_url, category):
    page = requests.get(product_page_url)
    soup = BeautifulSoup(page.content, "html.parser")
    if page.ok:

        table = soup.find("table", "table table-striped")
        rows = table.find_all("tr")
        data = []
        for row in rows:
            cols = row.find_all("td")
            for item in cols:
                item = item.text
                data.append(item)

        upc = data[0]
        price_including_tax = data[2]
        price_excluding_tax = data[3]
        extracted_number = re.findall(r"\d+", data[5])
        number_available = extracted_number[0]
        title = soup.find("li", class_="active").text
        on_top_of_description = soup.find("div", class_="sub-header")
        description = on_top_of_description.find_next("p").text
        image = soup.find("div", class_="item active").img
        image_path = image["src"]
        image_url = "http://books.toscrape.com" + image_path[5:]
        review_rating_tag = soup.find("p", "star-rating").attrs
        review_rating_letter = review_rating_tag["class"][1]
        review_rating = rating_in_letter_to_interger(review_rating_letter)
        product_data = [
            product_page_url,
            upc,
            title,
            price_including_tax,
            price_excluding_tax,
            number_available,
            description,
            category,
            review_rating,
            image_url,
        ]
        return product_data


# Scrap and return all category from the index
def get_all_categories(index):
    page = requests.get(index)
    soup = BeautifulSoup(page.content, "html.parser")
    links_containing_category = soup.find_all("a", href=re.compile("category"))
    categories = []
    for links in links_containing_category:
        full_path = links["href"]
        only_category = full_path[25:][:-11]
        categories.append(only_category)
    del categories[0]
    return categories


# Return all catalogue page's urls for a give category
def get_catalogue_urls_from_a_category(category):
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


# Scraps urls of product pages from a catalogue page


def get_page_product_url(catalogue_url):
    page = requests.get(catalogue_url)
    soup = BeautifulSoup(page.content, "html.parser")
    h3 = soup.find_all("h3")
    product_page_urls = []
    for titre in h3:
        path = titre.a["href"][8:]
        url = "https://books.toscrape.com/catalogue" + path
        product_page_urls.append(url)
    return product_page_urls
