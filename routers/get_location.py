from fastapi import APIRouter
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
import re
import requests
from bs4 import BeautifulSoup

router = APIRouter()

@router.get(
    "/location",
    tags=["Gold Price Calculator"]
    )
def get_location():

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



