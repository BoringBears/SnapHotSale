from bs4 import BeautifulSoup
import requests
import pandas as pd

df = pd.DataFrame(columns = ['Title',  'Price', 'Shipping', 'Qty Sold',  'Link', 'Img'])
n=0

source = requests.get('https://www.ebay.com/b/Cell-Phone-Smartphone-Parts/43304/bn_151926?rt=nc&_pgn=1').text    
soup = BeautifulSoup(source, 'lxml')
for item in soup.find_all('li', class_='s-item'):
    try:
        item_title = item.find('h3', class_='s-item__title').text
    except Exception as e:
        item_title = 'None'

    print(item_title)

    try:
        item_price = item.find('span', class_='s-item__price').text
    except Exception as e:
        item_price = 'None'

    print(item_price)

    try:
        item_shipping = item.find('span', class_='s-item__shipping s-item__logisticsCost').text
    except Exception as e:
        item_shipping = 'None'

    print(item_shipping)

    try:
        item_top_seller = item.find('span', class_='s-item__etrs-text').text
    except Exception as e:
        item_top_seller = 'None'

    print(item_top_seller)    

    try:
        item_stars = item.find('span', class_='clipped').text.split(' ')[0]
    except Exception as e:
        item_stars = 'None'

    print(item_stars)

    try:
        item_nreviews = item.find('a', class_='s-item__reviews-count').text.split(' ')[0]
    except Exception as e:
        item_nreviews = 'None' 

    print(item_nreviews)

    try:
        item_qty_sold = item.find('span', class_='s-item__hotness s-item__itemHotness').text.split(' ')
        if item_qty_sold[1] == 'sold':
            item_qty_sold = item_qty_sold[0]
        else:
            item_qty_sold = 0
    except Exception as e:
        item_qty_sold = 'None'

    print(item_qty_sold)

    try:
        item_link = item.find('a', class_='s-item__link')['href']
    except Exception as e:
        item_link = 'None'

    print(item_link)

    try:
        item_img = item.find('img', class_='s-item__image-img').get('data-src')
    except Exception as e:
        item_img = 'None'

    print(item_img)
    print()
    df.loc[n, 'Title'] = item_title
    df.loc[n, 'Price'] = item_price
    df.loc[n, 'Shipping'] = item_shipping
    df.loc[n, 'Top Seller'] = item_top_seller
    df.loc[n, 'Stars'] = item_stars
    df.loc[n, 'No. Of Reviews'] = item_nreviews
    df.loc[n, 'Qty Sold'] = item_qty_sold
    df.loc[n, 'Link'] = item_link    
    df.loc[n, 'Img'] = item_img   
    
    n+=1

#df.to_excel('ebay_phones.xlsx')
df.to_csv('ebay_phones.csv')
