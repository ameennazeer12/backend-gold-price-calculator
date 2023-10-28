# Backend for Gold Price Calculator
Backend for Gold Price Calculator App

Welcome to the Backend for Gold Price Calculator project. This repository contains the server-side code for a FastAPI-based API's that calculates the buying cost of gold based on location, current gold price, weight in gms and making charge.

Deployed Url - https://backend-gold-price-calculator.onrender.com/docs (May take upto 1 min to load as Render(free service) has to spin up an backend instance).

## Project Overview

The Backend for Gold Price Calculator is designed to provide a RESTful API's that allows users to retrieve the current gold price and calculate the buying cost of gold. This project is built with FastAPI and uses requests and beautifulsoup4 libraries to fetch and parse the required real-time data. It fetches the latest gold price data from https://www.goodreturns.in/gold-rates/ and provides it to the clients in a structured format.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.7 or above
- Code Editor like VSCode

### Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/ameennazeer12/backend-gold-price-calculator.git
   cd gold-price-calculator-backend

2. Create a virtual environment

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use: venv\Scripts\activate

3. Install the required dependencies

    ```bash
    pip install -r requirements.txt

4. To run the Application, use the following command

    ```bash
    uvicorn main:app --reload

This will start the server, and the API's will be accessible at http://localhost:8000/docs.

Open API Spec can be found at http://localhost:8000/redoc.


### API Endpoints

1. /get-location-list

    Retrieves the locations available to get todays gold price 

2. /gold-price-by-location

    Based on the location we get todays gold price per gm 

3. /calculate-gold-buying-amount

    Calculates the gold buying amount based on the todays price, weight and making charge

## Credits

I would like to acknowledge the real time gold price is parsed from https://www.goodreturns.in/gold-rates/ website