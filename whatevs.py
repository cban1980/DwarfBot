#!/usr/bin/env python3 
import requests
from bs4 import BeautifulSoup as bs
url_data = requests.get('https://tools.idrinth.de/addons/').text
soup = bs(url_data, 'html.parser')
soupdivs = soup.findAll("div", {"class": "addonListing"},)
print(soupdivs)
