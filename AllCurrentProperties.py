from bs4 import BeautifulSoup
import requests
import pandas as pd 
from math import ceil
import os
import re

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
try:
    os.remove('All Property Listings.csv')
except FileNotFoundError:
    pass


state = input("Enter Name of State Abbreviation\nFor example, New York would be NY: ")
state = state.capitalize()
city = input("Enter full name of city: ")

WEBSITE = 'https://www.trulia.com/%(state)s/%(city)s/' % {"state": state.capitalize(), "city" : city }

headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62'})

response = requests.get(WEBSITE, headers = headers)

real_estate = pd.DataFrame(columns = ['Address', 'Beds', 'Baths', 'Price'])

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



for i in range(1, 10, 1): #10 is here so I can run the program without waiting a century. Feel free to change it to the value of total_homes or a random integer.
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

            if addy == None:
                continue
            else:
                if bath == None:
                    baths.append("Undisclosed")
                if bed == None:
                    beds.append("Undisclosed")
                addy = addy.text.strip()
                address.append(addy)
                if bed != None:
                    bed = bed.text.strip()
                    beds.append(bed)
                if bath != None:
                    bath = bath.text.strip()
                    baths.append(bath)
                if price != None:
                    price = price.text.strip()
                    prices.append(price)
                else:
                    prices.append('undisclosed')
                if squarefoot != None:
                    squarefoot = squarefoot.text.strip()
                    squarefoots.append(squarefoot)
                else:
                    squarefoots.append('Undisclosed')  
    except:
        print ('error has occurred')
        continue
    # print (len(squarefoots), len(address), len(beds), len(baths), len(prices))

for i in range (len(address)):
    try:
        real_estate=real_estate.append({'Address':address[i], 'Beds':beds[i], 'Baths':baths[i], 'Price':prices[i], 'Square Foot':squarefoots[i]}, ignore_index=True)
    except:
        continue
        
    
real_estate.to_csv('All Property Listings.csv')
