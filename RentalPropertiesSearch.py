from bs4 import BeautifulSoup
import requests
import pandas as pd 
from math import ceil
import os
import re

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
try:
    os.remove('Rental Search.csv')
except FileNotFoundError:
    pass

WEBSITE = 'https://www.trulia.com/%(state)s/%(city)s/' % {"state": state.capitalize(), "city" : city }

headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62'})

response = requests.get(WEBSITE, headers = headers)