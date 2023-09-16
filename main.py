from fastapi import FastAPI
from routers import get_location,get_gold_price_by_location,get_total_gold_cost

app = FastAPI()

app.include_router(get_location.router)
app.include_router(get_gold_price_by_location.router)
app.include_router(get_total_gold_cost.router)
