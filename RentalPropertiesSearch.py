from bs4 import BeautifulSoup
import requests
import pandas as pd 
import os
import sklearn as sk
from math import ceil
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

try:
    os.remove('Rental Search.csv')
except FileNotFoundError:
    pass


HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}



# state = input('Enter name of state (ex: Georgia): ')
# city = input('Enter name of city (ex: Atlanta): ')
state = 'GA'
city = 'Atlanta'

beds = '3'
bathrooms = 'ANY'
min_Price = '1400'
max_Price = '1700'

beds = '' if beds == 'ANY' else f'{beds}p_beds/'
bathrooms = '' if bathrooms == 'ANY' else f'{bathrooms}p_baths/'
 
price_Range = '' if min_Price == 'ANY' and max_Price == 'ANY' else \
              f'0-{max_Price}_price/' if min_Price == 'ANY' else \
              f'{min_Price}p_price/' if max_Price == 'ANY' else \
              f'{min_Price}-{max_Price}_price/'

WEBSITE = f'https://www.trulia.com/for_rent/{city},{state}/{beds}{bathrooms}{price_Range}'

response = requests.get(WEBSITE, headers = HEADERS)
if response.status_code != 200:
    print ('Check inputs')
    exit()

soup = BeautifulSoup(response.content, 'html.parser')

total_homes = soup.find('h2', {'class': 'SearchResultsHeadings__ResultCountText-sc-1npyos5-1 gRoetB'})

total_homes  = int(total_homes.text.strip(' rentals'))

totalpages = ceil(total_homes / 40)

addresses, beds, bathrooms, prices, squarefoots, links = [],[],[],[],[],[]


for i in range(1, 2, 1):
    WEBSITE = WEBSITE if i == 1 else f'{WEBSITE}{i}_p/'
    response = requests.get(WEBSITE, headers = HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    results = soup.find_all('li', {'class': 'Grid__CellBox-sc-144isrp-0 SearchResultsList__WideCell-sc-14hv67h-2 gBXIcq bmFlVd'})

    for listings in results:
        try:
            address = listings.find('div', {'data-testid': 'property-address'})
            bed = listings.find('div', {'data-testid': 'property-beds'})
            bath = listings.find('div', {'data-testid': 'property-baths'})
            price = listings.find('div', {'data-testid': 'property-price'})
            squarefoot = listings.find('div', {'data-testid', 'property-floorSpace'})
            link = listings.find('a', {'data-testid': 'property-card-link'})
            
            if address == None:
                continue
            else:
                bathrooms.append("Undisclosed") if bath is None else None
                beds.append("Undisclosed") if bed is None else None

                address.append(address.text.strip())
                beds.append(bed.text.strip()) if bed is not None else None
                bathrooms.append(bath.text.strip()) if bath is not None else None
                prices.append(price.text.strip()) if prices is not None else None
                squarefoots.append(squarefoot.text.strip()) if squarefoot is not None else None
                links.append(f"https://www.trulia.com/{link['href']}") if link is not None else None
        except:
            print ('error has occured')
            continue

real_estate = pd.DataFrame(columns = ['Address', 'Beds', 'Bathrooms', 'Price', 'Square Foot', 'Link'])

for i in range(len(addresses)):
    try:
        property_data = {
                            'Address': address[i],
                             'Beds': beds[i],
                             'Baths': bathrooms[i],
                             'Price': prices[i],
                             'Square Foot': squarefoots[i],
                             'Link': links[i]
                        }
        real_estate.append(property_data)
    except:
        continue





df = pd.DataFrame(real_estate)
df.to_csv('Rental Search.csv', index=False)
print(price_Range)


# # https://www.trulia.com/for_rent/Atlanta,GA/4p_beds/5p_baths/700-1300_price/


print (soup)
