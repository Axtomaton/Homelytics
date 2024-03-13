from fastapi import FastAPI
import uvicorn
import requests
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import re
import bs4 as beautifulsoup
from math import ceil
import requests
import json
import csv

STATE = "NY"
CITY = "New_York"
WEBSITE = f"https://www.trulia.com/{STATE}/{CITY}/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62"
}
URL = "https://www.trulia.com"

app = FastAPI()
# Set up CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.get("/states")
async def get_states():
    with open("json_data/states.json") as f:
        states = json.load(f)
        return states

# Define the root route
@app.get("/")
async def root():
    address_keyed_json = {}
    with open("json_data/nyc_data.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            address = row["Address"]  #Address will the key and everything else will the val. 
            property_details = {
                "Beds": row["Beds"],
                "Baths": row["Baths"],
                "Price": row["Price"],
                "SquareFoot": row["SquareFoot"],
                "href": row["href"],
                "img": row["img"]
            }
            address_keyed_json[address] = property_details
    return address_keyed_json
    
@app.post("/properties/{state}/{city}") #used to collect the data from the website
async def get_properties(state: str, city: str):
    website = f"https://www.trulia.com/{state}/{city}/"
    real_estate = pd.DataFrame(
        columns=["Address", "Beds", "Baths", "Price", "SquareFoot", "href", "img"]
    )
    response = requests.get(website, headers=HEADERS)
    if response.status_code != 200:
        print("Incorrect Parameters. Check the state abbreviation or city.")
        exit()

    soup = beautifulsoup(response.content, "html.parser")
    total_homes_element = soup.find("h2", class_="sc-259f2640-0 bcPATd")
    total_homes = int("".join(filter(str.isdigit, total_homes_element.text))) if total_homes_element else 0
    total_pages = ceil(total_homes / 40)  # Trulia has 40 properties per page. 
    for page_num in range(1, 20):  # Modify 20 to total_page if you want all results.
        try:
            page_url = website if page_num == 1 else f"{website}{page_num}_p/" 
            page_response = requests.get(page_url, headers=HEADERS)
            page_soup = beautifulsoup(page_response.content, "html.parser")
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
                    real_estate = real_estate.append({
                        "Address": address_elem.text.strip(),
                        "Beds": bed.text.strip() if bed else "Undisclosed",
                        "Baths": bath.text.strip() if bath else "Undisclosed",
                        "Price": price_elem.text.strip().replace("+", "").replace("$", "").replace(",", "") if price_elem else "undisclosed",
                        "SquareFoot": re.search(r"(\d{1,3}(,\d{3})*)(\.\d+)?\s+sqft(\s*\(on [0-9\.]+ acres\))?", square_foot_elem.text.strip()).group(1).replace(",", "") if square_foot_elem else "Undisclosed",
                        "href": href_elem,
                        "img": img_elem
                    }, ignore_index=True)
        except Exception as e:
            print(f"Error: {e}")
            continue
    
    real_estate_json = real_estate.set_index("Address").to_dict(orient="index")
    return json.dumps(real_estate_json)
    
@app.get("/filtered_data/{state}/{city}")
async def filteredData(pandas_df):
    '''
    '''


# Ensure the app runs only when this script is executed directly
if __name__ == "__main__":
    # uvicorn main:app --reload
    uvicorn.run(app, host="localhost", port=8080)
