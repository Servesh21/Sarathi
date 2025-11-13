import os
import requests
from langchain_core.tools import tool
from dotenv import load_dotenv

# Load .env file from the backend root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env'))

@tool
def find_nearby_mechanics(city: str) -> str:
    """
    Finds nearby auto mechanics/garages in a city using Google Places API.
    Returns top 3 mechanics as a simple numbered list, optimized for LLMs.
    """
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        return "Error: GOOGLE_MAPS_API_KEY_NOT_SET."
    
    # Using Google Places Text Search
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    query = f"auto mechanic {city}"
    
    params = {
        "query": query,
        "key": api_key,
        "fields": "name,rating,formatted_address",  # Minimal fields
        "type": "car_repair"
    }
    
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") != "OK":
            return "Error: NO_MECHANICS_FOUND."
        
        results = data.get("results", [])
        if not results:
            return "Error: NO_MECHANICS_FOUND."
        
        # Top 3 mechanics, minimal string format
        mechanics = []
        for i, place in enumerate(results[:3], 1):
            name = place.get("name", "Unknown")
            rating = place.get("rating", "N/A")
            address = place.get("formatted_address", "N/A")
            mechanics.append(f"{i}. {name} ({rating}★) - {address}")
        
        return "\n".join(mechanics)
        
    except requests.exceptions.RequestException:
        return "Error: FAILED_TO_FETCH_MECHANICS."

if __name__ == "__main__":
    print(find_nearby_mechanics("Mumbai"))