from fastapi import FastAPI, HTTPException
from sklearn.covariance import EllipticEnvelope
from sklearn.discriminant_analysis import StandardScaler
import uvicorn
import requests
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import re
from bs4 import BeautifulSoup
from math import ceil
import requests
import matplotlib.pyplot as plt


state = "NY"
city = "New York"  
city = city.replace(" ", "_") 
# print(city)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62"
}
URL = "https://www.trulia.com"

website = f"https://www.trulia.com/{state}/{city}/"
real_estate_data = []  # List to store property data

response = requests.get(website, headers=HEADERS)
if response.status_code != 200:
    raise HTTPException(status_code=404, detail="Incorrect Parameters. Check the state abbreviation or city.")

soup = BeautifulSoup(response.content, "html.parser")
total_homes_element = soup.find("h2", class_="sc-259f2640-0 bcPATd")
total_homes = int("".join(filter(str.isdigit, total_homes_element.text))) if total_homes_element else 0
total_pages = ceil(total_homes / 40)

for page_num in range(1, 20): #feel free to modify to use `total_pages` but it will take longer
    try:
        page_url = website if page_num == 1 else f"{website}{page_num}_p/"
        page_response = requests.get(page_url, headers=HEADERS)
        page_soup = BeautifulSoup(page_response.content, "html.parser")
        property_list = page_soup.find_all("li", class_="Grid__CellBox-sc-a8dff4e9-0 sc-84372ace-0 kloaJl kTTMdB")
        for property_elem in property_list:
            bed = property_elem.find("div", {"data-testid": "property-beds"})
            bath = property_elem.find("div", {"data-testid": "property-baths"})
            address_elem = property_elem.find("div", {"data-testid": "property-address"})
            price_elem = property_elem.find("div", {"data-testid": "property-price"})
            square_foot_elem = property_elem.find("div", {"data-testid": "property-floorSpace"})
            href_elem = property_elem.find("a", {"class": "Anchor__StyledAnchor-sc-3c3ff02e-1 doURDx"})
            href_elem = URL + href_elem["href"] if href_elem else "Undisclosed"
            img_elem = property_elem.find("img", {"class": "Image__ImageContainer-sc-7293ddb2-0 iAFCmM"})
            img_elem = img_elem["src"] if img_elem else "Undisclosed"
            if address_elem:
                property_data = {
                    "Address": address_elem.text.strip(),
                    "Beds": bed.text.strip() if bed else "Undisclosed",
                    "Baths": bath.text.strip() if bath else "Undisclosed",
                    "Price": price_elem.text.strip().replace("+", "").replace("$", "").replace(",", "") if price_elem else "undisclosed",
                    "SquareFoot": re.search(r"(\d{1,3}(,\d{3})*)(\.\d+)?\s+sqft(\s*\(on [0-9\.]+ acres\))?", square_foot_elem.text.strip()).group(1).replace(",", "") if square_foot_elem else "Undisclosed",
                    "href": href_elem,
                    "img": img_elem
                }
                real_estate_data.append(property_data)
                
    except Exception as e:
        print(f"Error: {e}")
        continue

real_estate = pd.DataFrame(real_estate_data)
real_estate.to_csv('nyc_data.csv', index=False)