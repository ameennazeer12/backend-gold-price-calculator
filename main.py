from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
import re
import requests
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/cities")
def read_cities():
    # Define the URL of the website you want to scrape
    url = 'https://www.goodreturns.in/gold-rates/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    # Send an HTTP GET request to the URL
    response = requests.get(url,headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the <div> element with class "gold_silver_table"
        gold_silver_tables = soup.find_all('div', class_='gold_silver_table')

        # Create an empty dictionary to store the data
        data_dict = {}

         # Iterate through each table
        for gold_silver_table in gold_silver_tables:
            # Find all the <tr> elements within the table (excluding the header row)
            rows = gold_silver_table.find_all('tr', class_=lambda x: x != 'first')

            # Iterate through the rows and extract data
            for row in rows:
                # Extract the country name
                country_element = row.find('a')
                if country_element:
                    country_name = country_element.text
                    # Extract the href attribute and remove ".html"
                    href_value = country_element.get('href').replace('.html', '')

                    # Store the data in the dictionary
                    data_dict[country_name] = href_value

        # Print the resulting dictionary
        print(data_dict)
        return {"cities": data_dict}
    else:
        print('Failed to retrieve the web page. Status code:', response.status_code)


@app.get("/current-gold-price/{city}")
def read_item(city: str):
    gold_price = ""
    # Define the URL of the website you want to scrape
        
    url = f"https://www.goodreturns.in/gold-rates/{city}.html"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    # Send an HTTP GET request to the URL
    response = requests.get(url,headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page using Beautiful Soup
        soup = BeautifulSoup(response.text, 'html.parser')


        # Find the <div id="current-price"> element
        current_price_div = soup.find('div', id='current-price')

        # Extract and print the content of the <div>
        if current_price_div:
            gold_price = current_price_div.text.strip()
            gold_price = gold_price.split('\n')[0].strip()
            print(f"Gold Price: {gold_price}")
        else:
            print(f"Couldn't find the 'current-price' div on the page.")
        

    else:
        print('Failed to retrieve the web page. Status code:', response.status_code)

    return {"gold_price": gold_price, "city": city}
    


@app.get("/calculate-gold-price/{gold_price}")
def calculate_gold_price(gold_price: str,weight_in_gms: float | None = None,making_charge: float | None = None):
    if weight_in_gms is None:
        weight_in_gms = 1
    if making_charge is None:
        making_charge = 0
    digits_only = re.sub(r'[^0-9]', '', gold_price)
    total_cost = int(digits_only) * weight_in_gms * (1 + making_charge/100)



    currency = " "
    # Use regular expression to extract the part before the first number
    match = re.search(r'[^0-9]*', gold_price)

    # Check if a match was found
    if match:
        part_before_first_number = match.group(0)
        currency = part_before_first_number.strip() + currency # Remove leading/trailing whitespace if needed

        
    return {"total_cost_gold": currency+str(total_cost)}
