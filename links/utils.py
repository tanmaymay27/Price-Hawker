import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import lxml

def get_link_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "Accept-Language": "en",
    }
    website  = urlparse(url).netloc
    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")

    #amazon
    
    if(website[4:5]=='a'):
        name = soup.select_one(selector="#productTitle").getText()
        name = name.strip()
        # print(name)

        price = soup.select_one(selector=".a-price-whole").getText()
        price = price.replace(",", "")
        price = float(price)

    # print(soup.prettify())

    #flipkart
    if(website[4:5]=='f'):
        name = soup.select_one(selector=".B_NuCI").getText()
        name = name.strip()
    # print(name)

        price = soup.select_one(selector="_30jeq3 _16Jk6d").getText()
        price = price[1:]
        price = price.replace(",", "")
        price = float(price)
    # print(price)

    return name, price