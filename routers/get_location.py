from fastapi import FastAPI, APIRouter
from typing import Union
from pydantic import BaseModel
import re
import requests
from bs4 import BeautifulSoup
from utils.response_util import ResponseUtil,ResponseOut,BadResponseOut
from utils.logger_util import LoggerUtil

router = APIRouter()

@router.get(
    "/get-location-list",
    tags=["Gold Price Calculator"],
    responses={
    200: {"model": ResponseOut},
    404: {"model": ResponseOut},
    500: {"model": BadResponseOut}
    },
    )

def get_location_list():
    try:
        # Define the URL of the website you want to scrape
        url = 'https://www.goodreturns.in/gold-rates/'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        try:
            # Send an HTTP GET request to the URL
            response = requests.get(url,headers=headers)
        except Exception as e:
            LoggerUtil.log_exception(method_name="get_location_list | requests.get",exception=str(e))
            return ResponseUtil.internal_server_response()

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            try:
                # Parse the HTML content of the page using BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find the <div> element with class "gold_silver_table"
                gold_silver_tables = soup.find_all('div', class_='gold_silver_table')

                # Create an empty dictionary to store the data
                location_dict = {}

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
                            location_dict[country_name] = href_value
            except Exception as e:
                LoggerUtil.log_exception(method_name="get_location_list | Parsing HTML Error",exception=str(e))
                return ResponseUtil.internal_server_response()

            # Print the resulting dictionary
            LoggerUtil.info(f"Location dictionary: {location_dict}")
            return ResponseUtil.api_response(
                data={"location_list": location_dict},
                message="Location list returned ",
                response_code="200",
                status_code=200
                )
        else:
            LoggerUtil.error(f"Failed to retrieve the web page. Status code: {response.status_code}")
            return ResponseUtil.api_response(
                message="Failed to retrieve location list",
                response_code="404",
                status_code=404
                )
    except Exception as e:
        LoggerUtil.log_exception(method_name="get_location_list",exception=str(e))
        return ResponseUtil.internal_server_response()



