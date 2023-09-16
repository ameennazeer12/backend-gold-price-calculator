from fastapi import APIRouter
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
import re
import requests
from bs4 import BeautifulSoup

router = APIRouter()

@router.get(
    "/total-gold-cost/{gold_price}",
    tags=["Gold Price Calculator"]
    )
def get_total_gold_cost(gold_price: str,weight_in_gms: Union[float, None] = None,making_charge: Union[float, None] = None):
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