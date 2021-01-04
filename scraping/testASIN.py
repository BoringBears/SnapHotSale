import re
url='https://www.amazon.com/Floral-Find-Womens-Sleeve-Leopard/dp/B07QM7WKSG/ref=sr_1_108_sspa?dchild=1&keywords=lightning+deals&qid=1609302613&sr=8-108-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEzTzJRTVBWOE1WWjQ1JmVuY3J5cHRlZElkPUEwODMyOTg3M0xZUFoxMVpMV09MSyZlbmNyeXB0ZWRBZElkPUEwNzIwNjYzT1NaRlc2TDc4TDY4JndpZGdldE5hbWU9c3BfYnRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ=='
if url.find("www.amazon") == -1:
    print("not amz url")
else:
    print("amz url")
    m = re.search('/(?:dp|o|gp|-)\/(B[0-9]{2}[0-9A-Z]{7}|[0-9]{9}(?:X|[0-9]))/', url)
    print('https://www.amazon.com'+m.group(0))

url2='https://www.ebay.com/itm/Samsung-QN75Q900TSFXZA-75-Class-QN75Q900T-QLED-8K-UHD-HDR-Smart-TV-2020/254742040479?_trkparms=5373%3A5000006400%7C5374%3ATech%7C5079%3A5000006400'
n = url2.split('?')
print(n[0]);
