import re
import datetime
import configparser
import os
from urllib.request import Request
from urllib.request import urlopen
from urllib.parse import urljoin
from subprocess import Popen, PIPE
import dateutil.parser
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from urllib.parse import unquote

now = datetime.datetime.now().replace(microsecond=0).isoformat()
df = pd.DataFrame(columns = ['Title', 'Price', 'Price_Origin', 'Link', 'Image', 'Retailer', 'TimeStamp', 'Source'])
n = 0

# read and parse config
config = configparser.ConfigParser()
config.read(['rfd.cfg', os.path.expanduser('~/.rfd.cfg')])
config = config['rfd']
rfdUrl = "https://forums.redflagdeals.com"
rfdSections = [section.strip() for section in config['sections'].split(',')]

pages = 3
for section in rfdSections:
    for i in range(pages+1):
        print(rfdUrl+section+str(i))
        userAgent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'}
        req = Request(rfdUrl+section+str(i), None, userAgent)
        res = urlopen(req, timeout=10).read().decode('utf-8', 'ignore')

        soup = BeautifulSoup(res, "lxml")

        for thread in soup.findAll("li", {"class" : "topic"}):
            # Get post date.
            firstPostSoup = thread.find("span", {"class":"first-post-time"})
            if not firstPostSoup: continue

            threadCreateDate = dateutil.parser.parse(firstPostSoup.string)
            rfdtime = threadCreateDate.replace(tzinfo=dateutil.tz.gettz('America/Toronto'))
            utctime = rfdtime.astimezone(dateutil.tz.tzutc())
            daysOld = (datetime.datetime.utcnow().replace(tzinfo=dateutil.tz.tzutc()) - utctime).days + 1

            # Get post votes.
            voteSoup = thread.find("dl", {"class":"post_voting"})
            if not voteSoup: continue

            votesStr = re.sub('[^0-9-]', '', voteSoup['data-total'])
            votes = int(votesStr if votesStr != '' else 0)

            # Get number of comments.
            postSoup = thread.find("div", {"class":"posts"})
            if not postSoup: continue
            posts = int(re.sub('[^0-9]', '', postSoup.string))

            # Get title.
            titleSoup = thread.find("h3", {"class" : "topictitle"})
            if not titleSoup: continue

            title = ""
            for part in titleSoup:
                if part.string is not None:
                    title += part.string.strip() + " "
            title = title.strip()
            title = title.replace(';', ' ')

            timeSensitiveDeal = any(needle in title.lower() for needle in ['lava', 'error'])

            if (not timeSensitiveDeal and votes < 5*daysOld and posts < 10*daysOld) or votes < 0: continue

            # Get topic tile link
            topicUrl = rfdUrl+titleSoup.find("a", {"class" : "topic_title_link"})['href']

            # Fetch post contents
            threadReq = Request(topicUrl, None, userAgent)
            threadContent = urlopen(threadReq, timeout=10).read().decode('utf-8', 'ignore')
            threadSoup = BeautifulSoup(threadContent, "lxml")
            for elem in threadSoup.findAll(['script', 'style']):
                elem.extract()

            dealSoup = threadSoup.find("div", {"class":"post_content"})
            if not dealSoup: continue

            offerDetail = dealSoup.find("dl", {"class":"post_offer_fields"})
            if not offerDetail: continue

            # need to have URL
            link = offerDetail.find('dd', {"class":"deal_link"})
            if not link: continue
            prodUrl = unquote(unquote(link.find('a').get('href')))
            if not prodUrl: continue

            # try to get price
            priceText = offerDetail.find('dt', text="Price:");
            if priceText is not None: 
                price = priceText.find_next("dd").text.replace('$','')
            else:
                price = ''

            # try to get retailer
            retailerText = offerDetail.find('dt', text="Retailer:");
            if retailerText is not None: 
                retailer = retailerText.find_next("dd").text
            else:
                retailer = ''

            # save if it's a good offer
            #print(title, price, prodUrl)
            df.loc[n, 'Title'] = title
            df.loc[n, 'Price'] = price
            df.loc[n, 'Price_Origin'] = ''
            df.loc[n, 'Link'] = prodUrl
            df.loc[n, 'Image'] = ''
            df.loc[n, 'Retailer'] = retailer
            df.loc[n, 'TimeStamp'] = now
            df.loc[n, 'Source'] = topicUrl

            n += 1

        
df.to_csv('results/result-rfd'+str(now)+'.csv')
