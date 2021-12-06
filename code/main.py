from functions import *
import time
# *todo: download image and save it in file

start_time = time.time()

page_to_scrap = "https://books.toscrape.com/"
data = []
for category in get_all_categories(page_to_scrap):
    i = 0
    y = 1
    page_catalogue = get_catalogue_urls_from_a_category(category)
    for page in page_catalogue:
        temp = []
        i += 1
        temp.extend(get_page_product_url(page))
        for item in temp:
            # print(category+' page '+str(i)+' livre '+ str(y) +':')
            y += 1
            # print(get_data_from_product_page(item,category))
            data.append(get_data_from_product_page(item, category))
print(data)
print("--- %s seconds ---" % (time.time() - start_time))
