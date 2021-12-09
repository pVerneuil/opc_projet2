from functions import *
import time
import csv

start_time = time.time()

page_to_scrap = "https://books.toscrape.com/"
data = []
i=1
for category in get_all_categories(page_to_scrap):
    pages_catalogue = get_catalogue_urls_from_a_category(category)
    for page in pages_catalogue:
        all_product_page= []
        all_product_page.extend(get_page_product_url(page))
        for item in all_product_page:
            data.append(get_data_from_product_page(item, category))
            print("book scraped: " +str(i))
            i+=1

print("done in: " + "--- %s seconds ---" % (time.time() - start_time))

header = [
    "product_page_url",
    "universal_ product_code",
    "title",
    "price_including_tax",
    "price_excluding_tax",
    "number_available",
    "product_description",
    "category",
    "review_rating",
    "image_url",
]
with open("data/data.csv", "w", newline='', encoding="utf-8") as fichier_csv:
    writer = csv.writer(fichier_csv, delimiter=",")
    writer.writerow(header)
    writer.writerows(data)
print("writting in cvs files done at: ")
print("--- %s seconds ---" % (time.time() - start_time))

for item in data:
    image_url = item[9]
    image_name = "data/images/" + item[1] + ".jpg"
    img_data = requests.get(image_url).content
    with open(image_name, "wb") as handler:
        handler.write(img_data)
    print("download image of "+item[2])

print("downloadind images done at: ")
print("--- %s seconds ---" % (time.time() - start_time))

