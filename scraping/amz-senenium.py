import csv 
from bs4 import BeautifulSoup
from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path
import time
import pandas as pd

df = pd.DataFrame(columns = ['Title', 'Price', 'Price_Origin', 'Link', 'Image', 'TimeStamp', 'Source'])
n = 0

def get_url(search_term):
    #template = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss_1'
    template = 'https://www.amazon.com/s?k={}'
    search_term = search_term.replace(' ','+')
    
    url = template.format(search_term)
    url += '&page={}'

    ts = int(time.time())   
    url += '&qid='+ str(ts)

    url += '&ref=sr_pg_{}'

    return url

def extract_record(item):
    atag = item.h2.a
    description = atag.text.strip()
    url = 'https://www.amazon.com' + atag.get('href')

    try:
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text
    except AttributeError:
        return
        
    try:
        rating = item.i.text
        review_count = item.find('span', {'class': 'a-size-base', 'dir': 'auto'}).text
    except AttributeError:
        rating = ''
        review_count = ''
    
    result = (description, price, rating, review_count, url)
    return result

def main(search_term):
    driver = webdriver.Chrome('./chromedriver')
    
    records = []
    url = get_url(search_term)
    for page in range(1,8):
        driver.get(url.format(page, page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})

        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)
    driver.close()

    with open('amz_results.csv', 'w', newline='', encoding='utf-8') as f:
        write = csv.writer(f)
        write.writerow(['Description', 'Price', 'Rating', 'ReviewCount', 'Url'])
        write.writerows(records)

main('lightning deals')
