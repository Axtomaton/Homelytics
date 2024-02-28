from bs4 import BeautifulSoup
import requests
import pandas as pd 
import sklearn
from math import ceil
import os
import re

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
try:
    os.remove('All Current Properties.csv')
except FileNotFoundError:
    pass


state = input("Enter Name of State Abbreviation\nFor example, New York would be NY: ")
state = state.capitalize()
city = input("Enter full name of city: ")

WEBSITE = f'https://www.trulia.com/{state}/{city}/'

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62'}

response = requests.get(WEBSITE, headers = HEADERS)

if response.status_code != 200:
    print('Incorrect Parameters. Check the state abbreviation or city.')
    exit()

real_estate = pd.DataFrame(columns = ['Address', 'Beds', 'Baths', 'Price', 'Square Foot'])

soup = BeautifulSoup(response.content, 'html.parser')

total_homes = soup.find('h2', {'class':'SearchResultsHeadings__ResultCountText-sc-1npyos5-1 gRoetB'})

total_homes = total_homes.text.strip(' homes')


total_homes = int(total_homes.replace(',', ''))
total_homes = ceil(total_homes/40) #Divide by 40, since that is the amount per page.


addresses, beds, baths, prices, squarefoots = [], [], [], [], []



for i in range(1, 20, 1): #10 is here so I can run the program without waiting a century. Feel free to change it to the value of total_homes or a random integer. Or just total_homes + 1 for the entire database
    try:
        website = WEBSITE if i == 1 else WEBSITE + str(i) +'_p/'

        response = requests.get(website, headers = HEADERS)

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
                baths.append("Undisclosed") if bath is None else None
                beds.append("Undisclosed") if bed is None else None
                addy = addy.text.strip()
                addresses.append(addy)
                beds.append(bed.text.strip()) if bed is not None else None
                baths.append(bath.text.strip()) if bath is not None else None
                if price is not None:
                    if price.text.strip() == 'undisclosed' or price.text.strip() == '':
                        prices.append('undisclosed')
                    else:
                        prices.append(price.text.strip().replace('+','').replace('$','').replace(',',''))
                else:
                    prices.append('undisclosed')
                if squarefoot is not None and squarefoot.text.strip() != '':
                    sqft_match = re.search(r'(\d{1,3}(,\d{3})*)(\.\d+)?\s+sqft(\s*\(on [0-9\.]+ acres\))?', squarefoot.text.strip())
                    if sqft_match:
                        sqft_value = sqft_match.group(1).replace(",", "")
                        squarefoots.append(sqft_value)
                    else:
                        squarefoots.append('Undisclosed')
                else:
                    squarefoots.append('Undisclosed')
            
    except:
        continue
    
print(f'{len(addresses)} Properties found')

valid_indices = [i for i in range(len(addresses)) if squarefoots[i] != 'undisclosed' and prices[i] not in ['undisclosed', '']]
real_estate = []
for i in valid_indices:
    try:
        property_data = {   
                            'Address': addresses[i],
                            'Beds': beds[i],
                            'Baths': baths[i],
                            'Price': prices[i],
                            'Square Foot': squarefoots[i],
                        }
        real_estate.append(property_data)
    except:
        continue

df = pd.DataFrame(real_estate)
df.to_csv('All Current Properties.csv', index=False)

