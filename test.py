#!/usr/bin/env python3
import re
import requests
from bs4 import BeautifulSoup as bs
from urlextract import URLExtract
extractor = URLExtract()
url_data = requests.get('https://www.returnofreckoning.com/').text
soup = bs(url_data, 'html5lib')
soupdivs = soup.findAll("div", {"class": "faction_bar"},)
stringdivs = str(soupdivs)
urls = re.sub('amp;', '', stringdivs)
urls = extractor.find_urls(urls)
print(urls)