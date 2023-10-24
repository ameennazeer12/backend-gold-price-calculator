from fastapi import FastAPI, APIRouter
from typing import Union
from pydantic import BaseModel
import re
import requests
from bs4 import BeautifulSoup
from utils.response_util import ResponseUtil,ResponseOut,BadResponseOut
from utils.logger_util import LoggerUtil

router = APIRouter()

class BuyingGoldRequest(BaseModel):
    gold_price_today: str
    weight_in_gms: Union[float, None] = None
    making_charge: Union[float, None] = None

@router.post(
    "/calculate-gold-buying-amount",
    tags=["Gold Price Calculator"],
    responses={
        200: {"model": ResponseOut},
        500: {"model": BadResponseOut}
    },
    )
def calculate_gold_buying_amount(buying_gold_request: BuyingGoldRequest):
    try:
        gold_price_today, weight_in_gms, making_charge = buying_gold_request.gold_price_today, buying_gold_request.weight_in_gms, buying_gold_request.making_charge
        if weight_in_gms is None:
            weight_in_gms = 1
        if making_charge is None:
            making_charge = 0
        digits_only = re.sub(r'[^0-9.]', '', gold_price_today)
        total_cost = float(digits_only) * weight_in_gms * (1 + making_charge/100)
        currency = " "
        # Use regular expression to extract the part before the first number
        match = re.search(r'[^0-9]*', gold_price_today)

        # Check if a match was found
        if match:
            part_before_first_number = match.group(0)
            currency = part_before_first_number.strip() + currency # Remove leading/trailing whitespace if needed

        return ResponseUtil.api_response(
            data={"gold_buying_amount": currency+str(total_cost)},
            message="Today's gold price for the requested location returned",
            response_code="200",
            status_code=200
            )

    except Exception as e:
        LoggerUtil.log_exception(method_name="calculate_gold_buying_amount",exception=str(e))
        return ResponseUtil.internal_server_response()