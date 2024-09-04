# MARKETSTACK_KEY=73bbc69e222b690161c1f0ad1ebc0f39
import os
import requests
import json

API_KEY = os.environ.get('MARKETSTACK_KEY')
BASE_URL = "http://api.marketstack.com/v1"

def get_stock_price(stock_symbol):
    if not API_KEY:
        raise ValueError("API_KEY is not set in environment variables")
    
    params = {
        "access_key": API_KEY,
    }
    end_point = f"{BASE_URL}/tickers/{stock_symbol}/intraday/latest"
    api_result = requests.get(end_point, params=params)

    if api_result.status_code != 200:
        raise ValueError(f"Error fetching data: {api_result.status_code} - {api_result.text}")
    
    json_result = api_result.json()

    if "last" not in json_result:
        raise KeyError("Stock price not available")

    return {
        "last_price": json_result["last"]
    }