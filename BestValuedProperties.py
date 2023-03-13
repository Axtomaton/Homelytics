from bs4 import BeautifulSoup
import requests
import pandas as pd 
from math import ceil
import os
import re

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
try:
    os.remove('Best Value Properties.csv')
except FileNotFoundError:
    pass


state = input("Enter Name of State Abbreviation\nFor example, New York would be NY: ")
state = state.capitalize()
city = input("Enter full name of city: ")

WEBSITE = f'https://www.trulia.com/{state}/{city}/'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62'}
session = requests.Session()

response = requests.get(WEBSITE, headers = headers)

if response.status_code != 200:
    print('Incorrect Parameters. Check the state abbreviation or city.')
    exit()

real_estate = pd.DataFrame(columns = ['Address', 'Beds', 'Baths', 'Price', 'Square Foot', 'Suggested Price'])

soup = BeautifulSoup(response.content, 'html.parser')

total_homes = soup.find('h2', {'class':'SearchResultsHeadings__ResultCountText-sc-1npyos5-1 gRoetB'})

total_homes = total_homes.text.strip(' homes')


total_homes = int(total_homes.replace(',', ''))
total_homes = ceil(total_homes/40) #Divide by 40, since that is the amount per page.


address = []
beds = []
baths = []
prices = []
squarefoots = []
total_Prices = 0
total_SqFt = 0


for i in range(1, 20, 1): #10 is here so I can run the program without waiting a century. Feel free to change it to the value of total_homes or a random integer. Or just total_homes + 1 for the entire database
    try:
        if i == 1:
            website = WEBSITE
        else:
            website = WEBSITE + str(i) +'_p/'

        headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62'})

        response = requests.get(website, headers=headers)

        soup = BeautifulSoup(response.content, 'html.parser')

        result_update = soup.find_all('li', {'class' : 'Grid__CellBox-sc-144isrp-0 SearchResultsList__WideCell-sc-14hv67h-2 gBXIcq bmFlVd'})

        for result in result_update:
            bed = result.find('div', {'data-testid':'property-beds'})
            bath = result.find('div', {'data-testid':'property-baths'})
            addy = result.find('div', {'data-testid':'property-address'})
            price = result.find('div', {'data-testid': 'property-price'})
            squarefoot =  result.find('div', {'data-testid': 'property-floorSpace'})

            if addy is None:
                continue
            else:
                if bath is None:
                    baths.append("Undisclosed")
                if bed is None:
                    beds.append("Undisclosed")
                addy = addy.text.strip()
                address.append(addy)
                if bed is not None:
                    bed = bed.text.strip()
                    beds.append(bed)
                if bath is not None:
                    bath = bath.text.strip()
                    baths.append(bath)
                if price is not None:
                    if price.text.strip() == 'undisclosed' or price.text.strip() == '':
                        prices.append('undisclosed')
                    else:
                        price = price.text.strip()
                        price = price.replace('+','')
                        price = price.replace('$','')
                        price = price.replace(',','')
                        prices.append(price)
                        total_Prices += int(price)
                else:
                    prices.append('undisclosed')
                if squarefoot is not None and squarefoot.text.strip() != '':
                    squarefoot = squarefoot.text.strip()
                    sqft_match = re.search(r'(\d{1,3}(,\d{3})*)(\.\d+)?\s+sqft(\s*\(on [0-9\.]+ acres\))?', squarefoot)
                    if sqft_match:
                        sqft_value = sqft_match.group(1).replace(",", "")
                        total_SqFt += int(sqft_value)
                        squarefoots.append(sqft_value)
                else:
                    squarefoots.append('Undisclosed')
    except:
        continue
        # print (i)
    # print (len(squarefoots), len(address), len(beds), len(baths), len(prices))


price_per_sqft = total_Prices / total_SqFt

print(f"Price Per SquareFoot in {city}, {state.capitalize()} is {price_per_sqft}")

for i in range(len(address)):
    try:
        if squarefoots[i] == 'undisclosed' or prices[i] == 'undisclosed' or prices[i] == '':
            continue
        else:
            if float(squarefoots[i]) * price_per_sqft > float(prices[i]):
                real_estate = real_estate.append({
                    'Address': address[i],
                    'Beds': beds[i],
                    'Baths': baths[i],
                    'Price': prices[i],
                    'Square Foot': squarefoots[i],
                    'Suggested Price': round((float(squarefoots[i]) * price_per_sqft), 2)
                }, ignore_index=True)
            else:
                continue
    except:
        continue

real_estate.to_csv('Best Value Properties.csv', index=False)

