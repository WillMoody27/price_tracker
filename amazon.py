from bs4 import BeautifulSoup
import requests
import math
import datetime
import os  # checking file
import csv

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}


def bb_price_tracker():
    url = f'https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&browsedCategory=pcmcat1498066426386&id=pcat17071&iht=n&ks=960&list=y&qp=brand_facet%3DBrand~Apple%5Ecurrentoffers_facet%3DCurrent%20Deals~On%20Sale&sc=Global&st=pcmcat1498066426386_categoryid%24pcmcat144700050004&type=page&usc=All%20Categories'

    req = requests.get(url, headers=headers).content
    soup = BeautifulSoup(req, 'html.parser')

    # list of products
    ol_prod_list = soup.find("ol", {'class': 'sku-item-list'})

    # Product
    prod_list_name = ol_prod_list.findAll('h4', class_='sku-header')

    # price
    price_div = ol_prod_list.findAll('div', class_='priceView-hero-price priceView-customer-price')[:-1]
    price = ol_prod_list.findAll('span', class_='sr-only')

    # Savings + Reg Price
    prev_price_content = ol_prod_list.findAll('div', {'class': 'pricing-price__savings-regular-price'})[:-1]

    # grab the first price from block
    wp_div = ol_prod_list.findAll('div', class_='pricing-price__regular-price sr-only')

    file_exists = True

    if not os.path.exists('./price.cvs'):
        file_exists = False

    with open('price.csv', 'a') as file:
        writer = csv.writer(file, lineterminator='\n')
        # create row and columns
        fields = ['Timestamp', 'Product Name', 'Sale Price(USD)', 'Regular Price(USD)', 'Savings(USD)']

        # if it does not exist then write to file
        if not file_exists:
            writer.writerow(fields)

        for reg in range(len(prev_price_content)):
            print('-----------------------------------------------------------------------------')
            print(4 * '-', 'Product' + 4 * '-')

            prod_name = prod_list_name[reg].get_text()
            original_price = float(wp_div[reg].get_text().replace('The previous price was $', ''))
            sale_price = float(price[reg].get_text().replace('Your price for this item is $', ''))
            savings = math.floor(original_price - sale_price)

            print(prod_name)
            print(f"Sale: ${sale_price}")
            print(f'Reg: ${original_price}')
            print(f'Savings: ${savings}')

            # change this format later
            timestamp = f'{datetime.datetime.date(datetime.datetime.now())}, {datetime.datetime.time(datetime.datetime.now())}'
            writer.writerow([timestamp, prod_name, sale_price, original_price, savings])
            print('Finished exporting to cvs file.... ')


bb_price_tracker()
