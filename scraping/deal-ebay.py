from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime
from urllib.parse import unquote

now = datetime.datetime.now().replace(microsecond=0).isoformat()

df = pd.DataFrame(columns = ['Title', 'Price', 'Price_Origin', 'Link', 'Image', 'Retailer', 'TimeStamp', 'Source'])
cnt = 0

url = 'https://www.ebay.com/deals/tech'
response = requests.get(url)    
soup = BeautifulSoup(response.text, 'html.parser')

# feature deals
deals = soup.find_all(class_="ebayui-dne-item-featured-card")

def getDeal(category, n):
    if category == 'feature':
        deals = soup.find_all(class_="ebayui-dne-item-featured-card")
    elif category == 'card':
        deals = soup.find_all(class_="ebayui-dne-item-pattern-card")
    else:
        print("not support")

    for deal in deals:
        sections = deal.find_all(class_="col")
        for section in sections:
            block = section.find(class_="dne-itemtile-detail")
            item_title = block.find(class_="dne-itemtile-title")
            if item_title is not None:
                item_title = item_title["title"]
            else:
                continue
            
            link = block.find('a', class_="dne-itemtile-link")
            if not link: continue
            item_link = unquote(unquote(link['href'])).split('?')[0]
            #print(item_link)
            
            price = block.find(class_="dne-itemtile-price")
            if price is not None:
                item_price = price.text.replace('$','')
            else:
                continue
            #print(item_price)

            price_org = block.find(class_="dne-itemtile-original-price")
            if price_org is not None:
                item_price_org = price_org.find(class_="itemtile-price-strikethrough").text.replace('$','')
            else:
                item_price_org = '0'
            #print(item_price_org)
            if category == 'feature':
                item_img = section.find(class_="slashui-image-cntr").find('img').get('src')
            elif category == 'card':
                item_img = section.find(class_="slashui-image-cntr").find('img').get('data-config-src')
                deals = soup.find_all(class_="ebayui-dne-item-pattern-card")
            else:
                item_img = ''

            df.loc[n, 'Title'] = item_title
            df.loc[n, 'Price'] = item_price
            df.loc[n, 'Price_Origin'] = item_price_org
            df.loc[n, 'Link'] = item_link    
            df.loc[n, 'Image'] = item_img   
            df.loc[n, 'Retailer'] = 'ebay'
            df.loc[n, 'TimeStamp'] = now   
            df.loc[n, 'Source'] = url

            n += 1
    return n

cnt = getDeal('feature', 0)
getDeal('card', cnt)

'''
# card deal
card_deals = soup.find_all(class_="ebayui-dne-item-pattern-card")
for deal in card_deals:
    sections = deal.find_all(class_="col")
    for section in sections:
        block = section.find(class_="dne-itemtile-detail")
        item_title = block.find(class_="dne-itemtile-title")
        if item_title is not None:
            item_title = item_title["title"]
        else:
            continue
        
        link = block.find('a', class_="dne-itemtile-link")
        if not link: continue
        item_link = unquote(unquote(link['href'])).split('?')[0]
        
        price = block.find(class_="dne-itemtile-price")
        if price is not None:
            item_price = price.text.replace('$','')
        else:
            continue
        #print(item_price)

        price_org = block.find(class_="dne-itemtile-original-price")
        if price_org is not None:
            item_price_org = price_org.find(class_="itemtile-price-strikethrough").text.replace('$','')
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
'''
df.to_csv('results/result-ebay'+str(now)+'.csv')
