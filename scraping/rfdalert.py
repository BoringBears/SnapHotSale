#!/usr/bin/python3

import sqlite3
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

config = configparser.ConfigParser()
config.read(['rfd.cfg', os.path.expanduser('~/.rfd.cfg')])
config = config['rfd']

conn = sqlite3.connect(config['db_path'])
c = conn.cursor()

#emails = [email.strip() for email in config['emails'].split(',')]

rfdUrl = "http://forums.redflagdeals.com"
rfdSections = [section.strip() for section in config['sections'].split(',')]

cnt=0
for section in rfdSections:
    for i in [1,2,3]:
        print(rfdUrl+section+str(i))
        userAgent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'}
        req = Request(rfdUrl+section+str(i), None, userAgent)
        content = urlopen(req, timeout=10).read().decode('utf-8', 'ignore')

        soup = BeautifulSoup(content, "lxml")

        for thread in soup.findAll("li", {"class" : "topic"}):
            # Get post date.
            firstPostSoup = thread.find("span", {"class":"first-post-time"})
            if not firstPostSoup: continue

            threadCreateDate = dateutil.parser.parse(firstPostSoup.string)
            rfdtime = threadCreateDate.replace(tzinfo=dateutil.tz.gettz('America/Toronto'))
            utctime = rfdtime.astimezone(dateutil.tz.tzutc())
            daysOld = (datetime.datetime.utcnow().replace(tzinfo=dateutil.tz.tzutc()) - utctime).days + 1
            cnt+=1

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

            timeSensitiveDeal = any(needle in title.lower() for needle in ['lava', 'error'])

            if (not timeSensitiveDeal and votes < 5*daysOld and posts < 10*daysOld) or votes < 0: continue

            # this is topic tile link
            topicUrl = rfdUrl+titleSoup.find("a", {"class" : "topic_title_link"})['href']

            # Check whether post is in the database.
            c.execute('''SELECT COUNT(*) FROM rfd WHERE topicurl=?''', (topicUrl,))
            if c.fetchone()[0] > 0: continue

            print("title="+ title + "  link=" + topicUrl + "  post= " + str(posts) + " vote=" + str(votes))

            # Fetch post contents
            threadReq = Request(topicUrl, None, userAgent)
            threadContent = urlopen(threadReq, timeout=10).read().decode('utf-8', 'ignore')
            threadSoup = BeautifulSoup(threadContent, "lxml")
            for elem in threadSoup.findAll(['script', 'style']):
                elem.extract()

            dealSoup = threadSoup.find("div", {"class":"post_content"})
            if not dealSoup: continue

            # Convert relative links to absolute links for rfd links
            #for a in dealSoup.findAll('a', href=True):
            #    a['href'] = urljoin(rfdUrl, a['href'])
            
            prodUrl=''
            offerDetail = dealSoup.find("div", {"class":"post_offer"})
            if not offerDetail: continue
            for url in offerDetail.findAll('a', href=True):
                prodUrl=url['href']
                print(prodUrl)
                break

            # validate valid Url exist..
            if not prodUrl: continue

            # save to database if it's a good offer
            c.execute('''INSERT INTO rfd VALUES (?,?,?)''', (topicUrl,title,prodUrl))
            print("write complete for "+title)

# write to DB
conn.commit()
conn.close()
print(cnt)
