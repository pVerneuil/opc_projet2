import requests;
from bs4 import BeautifulSoup
import re
import csv

#comments go there
def rating_in_letter_to_interger(rating_in_letter):
    numbers={"Zero":0, "One":1, "Two":2, "Three":3, "Four":4, "Five":5} 
    rating_int=numbers[rating_in_letter]
    return rating_int

#comments go there
def get_data_from_product_page(product_page_url,category):
    page=requests.get(product_page_url)
    soup=BeautifulSoup(page.content,'html.parser')
    if page.ok:
        
        table=soup.find('table',"table table-striped")
        rows = table.find_all('tr')
        data = []
        for row in rows:
            cols = row.find_all('td')
            for item in cols:
                item=item.text
                data.append(item)

        upc=data[0]
        price_including_tax=data[2]
        price_excluding_tax=data[3]
        extracted_number = re.findall(r'\d+', data[5])
        number_available=extracted_number[0]
        #title
        title=soup.find('li',class_='active').text
        #description
        on_top_of_description=soup.find('div', class_="sub-header")
        description=on_top_of_description.find_next('p').text
        #image_url
        image=soup.find('div',class_="item active").img
        image_path=image['src']
        image_url='http://books.toscrape.com'+image_path[5:] #supression des 5 premiers characteres
        #review_rating
        review_rating_tag=soup.find('p','star-rating').attrs #<-- revoie un dictionnaire ou la note est l'indice 1 dans la liste associer a la clé class
        review_rating_letter=review_rating_tag['class'][1]
        review_rating=rating_in_letter_to_interger(review_rating_letter)
        product_data=[product_page_url, upc, title, price_including_tax, price_excluding_tax, number_available,description, category,review_rating, image_url]
        return product_data


def get_all_categories():
    product_page_url='http://books.toscrape.com/index.html'
    page=requests.get(product_page_url)
    soup=BeautifulSoup(page.content,'html.parser')
    test=soup.find_all('a',href=re.compile("category"))
    categories=[]
    for links in test:
        full_path=links['href']
        temp0=full_path[25:]
        temp=temp0[:-11]
        categories.append(temp)
    del categories[0]
    return categories