from fastapi import APIRouter
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
import re
import requests
from bs4 import BeautifulSoup

router = APIRouter()

@router.get(
    "/gold-price-by-location/{location}",
    tags=["Gold Price Calculator"]
    )
def get_gold_price_by_location(location: str):
    gold_price = ""
    # Define the URL of the website you want to scrape
        
    url = f"https://www.goodreturns.in/gold-rates/{location}.html"
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

    return {"gold_price": gold_price, "location": location}
    