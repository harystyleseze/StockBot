import os
import requests
import json

# Retrieve the MarketStack API key from environment variables
API_KEY = os.environ.get('MARKETSTACK_KEY')

# Base URL for the MarketStack API
BASE_URL = "http://api.marketstack.com/v1"

def get_stock_price(stock_symbol):
    """
    Fetch the latest intraday stock price for the given stock symbol.

    Args:
        stock_symbol (str): The symbol of the stock (e.g., 'AAPL' for Apple).
    
    Returns:
        dict: A dictionary containing the last price of the stock.
    
    Raises:
        ValueError: If the API_KEY is not set or the API request fails.
        KeyError: If the stock price is not available in the API response.
    """

    # Ensure the API_KEY is set in environment variables
    if not API_KEY:
        raise ValueError("API_KEY is not set in environment variables")
    
    # Define the parameters for the API request
    params = {
        "access_key": API_KEY,
    }

    # Construct the API endpoint for the given stock symbol's latest intraday data
    end_point = f"{BASE_URL}/tickers/{stock_symbol}/intraday/latest"

    # Make a GET request to the MarketStack API
    api_result = requests.get(end_point, params=params)

    # Check if the request was successful (status code 200)
    if api_result.status_code != 200:
        raise ValueError(f"Error fetching data: {api_result.status_code} - {api_result.text}")
    
    # Parse the response as JSON
    json_result = api_result.json()

    # Check if the 'last' field (latest price) is present in the response
    if "last" not in json_result:
        raise KeyError("Stock price not available")

    # Return the last stock price in a dictionary
    return {
        "last_price": json_result["last"]
    }