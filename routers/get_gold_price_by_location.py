from fastapi import FastAPI, APIRouter
from typing import Union
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from utils.response_util import ResponseUtil,ResponseOut,BadResponseOut
from utils.logger_util import LoggerUtil

router = APIRouter()

class LocationRequest(BaseModel):
    location: str

@router.post(
    "/gold-price-by-location",
    tags=["Gold Price Calculator"],
    responses={
        200: {"model": ResponseOut},
        404: {"model": ResponseOut},
        500: {"model": BadResponseOut}
    },
    )

def get_gold_price_by_location(location_request: LocationRequest):
    try:
        location = location_request.location
        location_formatted = location.replace(" ","-")
        gold_price = ""
        # Define the URL of the website you want to scrape
        url = f"https://www.goodreturns.in/gold-rates/{location_formatted}.html"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        # Send an HTTP GET request to the URL
        try:
            response = requests.get(url,headers=headers)
        except Exception as e:
            LoggerUtil.log_exception(method_name="get_gold_price_by_location | requests.get",exception=str(e))
            return ResponseUtil.internal_server_response()

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
                LoggerUtil.info(f"Gold Price: {gold_price}")
            else:
                LoggerUtil.error(f"Couldn't find the 'current-price' div on the page.")
                return ResponseUtil.api_response(
                    data={"location": location},
                    message="Failed to retrieve the gold price for the requested location",
                    response_code="404",
                    status_code=404
                    )
        else:
            LoggerUtil.error(f"Failed to retrieve the web page. Status code: {response.status_code}")
            return ResponseUtil.api_response(
                data={"location": location},
                message="Failed to retrieve the gold price for the requested location",
                response_code="404",
                status_code=404
                )
        print(f"location3 {location}")
        return ResponseUtil.api_response(
                data={"gold_price": gold_price, "location": location},
                message="Today's gold price for the requested location returned",
                response_code="200",
                status_code=200
                )
         
    except Exception as e:
        LoggerUtil.log_exception(method_name="get_gold_price_by_location",exception=str(e))
        return ResponseUtil.internal_server_response()