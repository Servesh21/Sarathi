import os
import requests
from langchain_core.tools import tool
from dotenv import load_dotenv

# Load .env file from the backend root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env'))

@tool
def get_weather(city: str) -> str:
    """
    Fetches the current weather for a specified city.
    Returns a simple, human-readable string, OPTIMIZED for an LLM.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "Error: OPENWEATHER_API_KEY_NOT_SET."

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    
    try:
        response = requests.get(base_url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        description = data['weather'][0]['description']
        temp = data['main']['temp']
        
        # Optimized for LLM: "City: Temp, Description"
        return f"{city}: {temp}°C, {description}."
    except requests.exceptions.RequestException:
        return "Error: FAILED_TO_FETCH_WEATHER."

if __name__ == "__main__":
    print(get_weather("Mumbai"))
