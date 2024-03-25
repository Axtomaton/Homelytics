from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
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
import json
import csv
import matplotlib.pyplot as plt
import uuid
import os
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
    properties_list = []
    with open("json_data/nyc_data.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            property_details = {
                "Address": row["Address"],
                "Beds": row["Beds"],
                "Baths": row["Baths"],
                "Price": '{:,.0f}'.format(float(row["Price"])),                
                "SquareFoot": row["SquareFoot"],
                "href": row["href"],
                "img": row["img"]
            }
            properties_list.append(property_details)
    return properties_list
    
@app.get("/properties/{state}/{city}")
async def get_properties(state: str, city: str):
    website = f"https://www.trulia.com/{state}/{city}/"
    real_estate_data = []  # List to store property data
    city = city.replace(" ", "_")# Replace spaces with underscores b/c thats how Trulia URL is formatted
    # print(city)
    response = requests.get(website, headers=HEADERS)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Incorrect Parameters. Check the state abbreviation or city.")

    soup = BeautifulSoup(response.content, "html.parser")
    total_homes_element = soup.find("h2", class_="sc-259f2640-0 bcPATd")
    total_homes = int("".join(filter(str.isdigit, total_homes_element.text))) if total_homes_element else 0
    total_pages = ceil(total_homes / 40)

    for page_num in range(1, 5): #feel free to modify to use `total_pages` but it will take longer for places with a lot of listings like NYC, SF, LA, etc
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
    filtered_real_estate, median_value_score = filter_data(real_estate)

    # Reset index to ensure uniqueness
    real_estate = real_estate.reset_index(drop=True) 
    chart_id = str(uuid.uuid4()) # Generate a unique chart ID
    real_estate["Price"] = real_estate["Price"].apply(lambda x: '{:,.0f}'.format(float(x)))


    return {"properties": real_estate.to_dict(orient="records"), 
            "filtered_properties": filtered_real_estate.to_dict(orient="records"), 
            "median_value_score": float(median_value_score), 
            "basic_stats": generateStats(filtered_real_estate),
            "chart": generateCharts(filtered_real_estate, chart_id),
            "chart_id": chart_id}

@app.get("/charts/{chart_id}")
async def get_chart(chart_id: str):
    chart_path = os.path.join("charts", f"{chart_id}.png")
    if os.path.exists(chart_path):
        return FileResponse(chart_path, media_type="image/png")
    else:
        raise HTTPException(status_code=404, detail="Chatr was not found!")

def filter_data(dataframe):
    # Drop rows with 'Undisclosed' values in the Price and SquareFoot cols
    dataframe = dataframe[dataframe['Price'] != 'Undisclosed']
    dataframe = dataframe[dataframe['SquareFoot'] != 'Undisclosed']

    dataframe['Price'] = pd.to_numeric(dataframe['Price'], errors='coerce')
    dataframe['SquareFoot'] = pd.to_numeric(dataframe['SquareFoot'], errors='coerce')
    dataframe.dropna(subset=['Price', 'SquareFoot'], inplace=True)

    # Calculate value score: price per square foot
    dataframe['Value Score'] = dataframe['Price'] / dataframe['SquareFoot']
    # Convert 'Value Score' column to numpy array
    value_score_data = dataframe['Value Score'].values.reshape(-1, 1)
    scaler = StandardScaler()
    value_score_data_standardized = scaler.fit_transform(value_score_data)
    envelope = EllipticEnvelope(contamination=0.05)  # 5% contamination (adjust as needed)
    envelope.fit(value_score_data_standardized)
    outliers = envelope.predict(value_score_data_standardized)
    filtered_data = dataframe[outliers == 1]

    best_properties = filtered_data.sort_values(by='Value Score') #dictionary of the properties based on value score
    median_value_score = best_properties['Value Score'].median()  # Calculate median value score
    return best_properties, median_value_score  # Return both filtered DataFrame and median value score

def generateStats(dataframe) -> dict:
    stats = {}
    stats['Median Price'] = float(dataframe['Price'].median())
    stats['Standard Deviation of Price'] = float(dataframe['Price'].std())
    stats['Minimum Price'] = float(dataframe['Price'].min())
    stats['Maximum Price'] = float(dataframe['Price'].max())
    return stats


def generateCharts(dataframe, chart_id):
    if 'Value Score' not in dataframe.columns:
        print("Error: 'Value Score' column not found in DataFrame")
        return None

    plt.figure(figsize=(10, 6))
    plt.hist(dataframe['Value Score'], bins=30, color='skyblue', edgecolor='black')
    plt.title('Distribution of Value Score')
    plt.xlabel('Value Score')
    plt.ylabel('Frequency')
    plt.grid(True)

    # Create the 'charts' directory if it doesn't exist
    charts_dir = 'charts'
    if not os.path.exists(charts_dir):
        os.makedirs(charts_dir)

    # Save the plot to the 'charts' directory with the provided chart_id
    chart_path = os.path.join(charts_dir, f"{chart_id}.png")
    plt.savefig(chart_path, format='png')
    plt.close()  # Close the plot to release resources
    return chart_path


if __name__ == "__main__":
    # uvicorn main:app --reload
    uvicorn.run(app, host="localhost", port=8080)
