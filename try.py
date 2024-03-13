from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from fake_useragent import UserAgent
from selenium.webdriver.support import expected_conditions as EC
import requests
import bs4 as beautifulsoup
import pandas as pd
from math import ceil

STATE = "NY"
CITY = "New_York"

def main():
    url = f"https://www.trulia.com/{STATE}/{CITY}/"
    real_estate = pd.DataFrame(columns = ['Address', 'Beds', 'Baths', 'Price', 'Square Foot'])
    address, beds, baths, price, square_foot = [], [], [], [], []
    response = requests.get(url)
    if response.status_code != 200:
        print('Incorrect Parameters. Check the state abbreviation or city.')
        exit()
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    ua = UserAgent()
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36'
    # options.add_argument('user-agent={0}'.format(user_agent))
    options.add_argument('user-agent={0}'.format(ua.random))
    # print('user-agent={0}'.format(ua.random))
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    pageContent = driver.page_source
    soup = beautifulsoup.BeautifulSoup(pageContent, 'html.parser')
    # print
    totalHomes = soup.find('h2', attrs={"class": "sc-259f2640-0 bcPATd"})
    # print(totalHomes)
    totalHomes = int(''.join(filter(lambda x: x.isdigit(), totalHomes.text))) #looks good
    totalPages = ceil(totalHomes/40) #Divide by 40, since that is the amount per page. This represent the amount of pages to go through.

    for i in range(1, 20, 1): #20 is here so it doesn't go through the 400 pages like w/ New York, NY.
        try:
            '''
            '''
        


        except Exception as e:
            return e

        finally:
            driver.quit()




if __name__ == "__main__":
    main()