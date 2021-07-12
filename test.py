#!/usr/bin/env python3
import re
import requests
from bs4 import BeautifulSoup as bs
from urlextract import URLExtract
extractor = URLExtract()
url_data = requests.get('https://www.returnofreckoning.com/').text
soup = bs(url_data, 'html5lib')
soupdivs = soup.findAll('div', attrs={'style': 'margin: 5px 0 2px 0;'})
soupdivs = str(soupdivs)
soupdivs = soupdivs[:-9]
soupdivs = soupdivs.split('>')[-1]
print(soupdivs)