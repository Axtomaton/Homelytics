import re
from math import ceil

import bs4 as beautifulsoup
import pandas as pd
import requests

STATE = "NY"
CITY = "New_York"
WEBSITE = f"https://www.trulia.com/{STATE}/{CITY}/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62"
}
URL = "https://www.trulia.com"


def main():
    realestate = pd.DataFrame(
        columns=["Address", "Beds", "Baths", "Price", "Square Foot", "href"]
    )
    address, beds, baths, price, square_foot, href, img = [], [], [], [], [], [], []

    response = requests.get(WEBSITE, headers=HEADERS)
    if response.status_code != 200:
        print("Incorrect Parameters. Check the state abbreviation or city.")
        return

    soup = beautifulsoup.BeautifulSoup(response.content, "html.parser")
    total_homes_element = soup.find("h2", class_="sc-259f2640-0 bcPATd")
    total_homes = (
        int("".join(filter(str.isdigit, total_homes_element.text)))
        if total_homes_element
        else 0
    )
    total_pages = ceil(total_homes / 40)  # Assuming 40 properties per page

    for page_num in range(
        1, 20
    ):  # Change to total_pages if you want to iterate over all pages
        try:
            page_url = WEBSITE if page_num == 1 else f"{WEBSITE}{page_num}_p/"
            page_response = requests.get(page_url, headers=HEADERS)
            page_soup = beautifulsoup.BeautifulSoup(
                page_response.content, "html.parser"
            )
            property_list = page_soup.find_all(
                "li", class_="Grid__CellBox-sc-a8dff4e9-0 sc-84372ace-0 kloaJl kTTMdB"
            )

            for property_elem in property_list:
                bed = property_elem.find("div", {"data-testid": "property-beds"})
                bath = property_elem.find("div", {"data-testid": "property-baths"})
                address_elem = property_elem.find(
                    "div", {"data-testid": "property-address"}
                )
                price_elem = property_elem.find(
                    "div", {"data-testid": "property-price"}
                )
                square_foot_elem = property_elem.find(
                    "div", {"data-testid": "property-floorSpace"}
                )
                href_elem = property_elem.find(
                    "a", {"class": "Anchor__StyledAnchor-sc-3c3ff02e-1 doURDx"}
                )
                href_elem = URL + href_elem["href"] if href_elem else "Undisclosed"
                img_elem = property_elem.find("img", {"class": "Image__ImageContainer-sc-7293ddb2-0 iAFCmM"})
                img_elem = img_elem["src"] if img_elem else "Undisclosed"


                if address_elem:
                    href.append(href_elem) if href_elem else "Undisclosed"
                    address.append(address_elem.text.strip())
                    img.append(img_elem)
                    beds.append(bed.text.strip() if bed else "Undisclosed")
                    baths.append(bath.text.strip() if bath else "Undisclosed")
                    price_text = (
                        price_elem.text.strip() if price_elem else "undisclosed"
                    )
                    price.append(
                        price_text.replace("+", "").replace("$", "").replace(",", "")
                    )

                    if square_foot_elem:
                        sqft_match = re.search(
                            r"(\d{1,3}(,\d{3})*)(\.\d+)?\s+sqft(\s*\(on [0-9\.]+ acres\))?",
                            square_foot_elem.text.strip(),
                        )
                        if sqft_match:
                            sqft_value = sqft_match.group(1).replace(",", "")
                            square_foot.append(sqft_value)
                        else:
                            square_foot.append("Undisclosed")
                    else:
                        square_foot.append("Undisclosed")
        except Exception as e:
            print(f"Error: {e}")
            continue

    realestate["Address"] = address
    realestate["Beds"] = beds
    realestate["Baths"] = baths
    realestate["Price"] = price
    realestate["Square Foot"] = square_foot
    realestate["href"] = href
    realestate["img"] = img
    return realestate
    # realestate.to_csv("realestate.csv", index=False)
    # print(realestate)

def filterData(dataframe):
    """
    """


if __name__ == "__main__":
    main()
