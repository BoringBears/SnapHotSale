from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime

now = datetime.datetime.now().replace(microsecond=0).isoformat()

df = pd.DataFrame(columns = ['Title', 'Price', 'Price_Origin', 'Link', 'Image', 'Retailer', 'TimeStamp', 'Source'])
n = 0

url = 'https://www.ebay.com/deals/tech'
response = requests.get(url)    
soup = BeautifulSoup(response.text, 'html.parser')

# feature deals
deals = soup.find_all(class_="ebayui-dne-item-featured-card")

for deal in deals:
    sections = deal.find_all(class_="col")
    for section in sections:
        block = section.find(class_="dne-itemtile-detail")
        item_title = block.find(class_="dne-itemtile-title")["title"]
        #print(item_title)
        
        item_link = block.find('a', class_="dne-itemtile-link")['href']
        #print(item_link)
        
        price = block.find(class_="dne-itemtile-price")
        if price is not None:
            item_price = price.text
        else:
            continue
        #print(item_price)

        price_org = block.find(class_="dne-itemtile-original-price")
        if price_org is not None:
            item_price_org = price_org.find(class_="itemtile-price-strikethrough").text
        else:
            item_price_org = '0'
        #print(item_price_org)
        
        item_img = section.find(class_="slashui-image-cntr").find('img').get('src')
        #print(item_img)

        df.loc[n, 'Title'] = item_title
        df.loc[n, 'Price'] = item_price
        df.loc[n, 'Price_Origin'] = item_price_org
        df.loc[n, 'Link'] = item_link    
        df.loc[n, 'Image'] = item_img   
        df.loc[n, 'Retailer'] = 'ebay'
        df.loc[n, 'TimeStamp'] = now   
        df.loc[n, 'Source'] = url

        n += 1

# card deal
card_deals = soup.find_all(class_="ebayui-dne-item-pattern-card")
for deal in card_deals:
    sections = deal.find_all(class_="col")
    for section in sections:
        block = section.find(class_="dne-itemtile-detail")
        item_title = block.find(class_="dne-itemtile-title")["title"]
        #print(item_title)
        
        item_link = block.find('a', class_="dne-itemtile-link")['href']
        #print(item_link)
        
        price = block.find(class_="dne-itemtile-price")
        if price is not None:
            item_price = price.text
        else:
            continue
        #print(item_price)

        price_org = block.find(class_="dne-itemtile-original-price")
        if price_org is not None:
            item_price_org = price_org.find(class_="itemtile-price-strikethrough").text
        else:
            item_proce_org = '0'
        #print(item_price_org)
        
        item_img = section.find(class_="slashui-image-cntr").find('img').get('data-config-src')
        #print(item_img)

        df.loc[n, 'Title'] = item_title
        df.loc[n, 'Price'] = item_price
        df.loc[n, 'Price_Origin'] = item_price_org
        df.loc[n, 'Link'] = item_link    
        df.loc[n, 'Image'] = item_img   
        df.loc[n, 'Retailer'] = 'ebay'
        df.loc[n, 'TimeStamp'] = now   
        df.loc[n, 'Source'] = url

        n += 1

df.to_csv('results/result-ebay'+str(now)+'.csv')
