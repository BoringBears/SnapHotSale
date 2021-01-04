import csv, sqlite3

# connect DB
con = sqlite3.connect("/home/auser/workspace/SnapHotSale/django-spider/db.sqlite3") # change to 'sqlite:///your_filename.db'
cur = con.cursor()

#read csv
with open('results/mergedAll.csv','r') as fin: # `with` statement available in 2.5+
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['Title'], i['Price'], i['Price_Origin'], i['Link'], i['Image'], i['Retailer'],i['TimeStamp'], i['Source']) for i in dr]

cur.executemany("INSERT INTO showdeals_dealinfo ('title', 'price', 'price_origin', 'link', 'image', 'retailer', 'timestamp', 'source') VALUES (?,?,?,?,?,?,?,?);", to_db)

#cur.execute("SELECT * FROM showdeals_dealinfo")
#print(cur.fetchall())
con.commit()
con.close()
