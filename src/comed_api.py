"""
ComEd Hourly Pricing API Client
Fetches current electricity prices from ComEd's public API.
"""

import requests
from typing import Optional


def get_current_price() -> Optional[float]:
    """
    Fetch the current hour average price from ComEd.
    
    Returns:
        Price in cents/kWh, or None if the API call fails.
    """
    url = "https://hourlypricing.comed.com/api?type=currenthouraverage"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data and len(data) > 0:
            return float(data[0]["price"])
        return None
        
    except (requests.RequestException, KeyError, ValueError, IndexError) as e:
        print(f"Error fetching ComEd price: {e}")
        return None


if __name__ == "__main__":
    price = get_current_price()
    if price is not None:
        print(f"Current ComEd price: {price}¢/kWh")
    else:
        print("Failed to fetch price")
