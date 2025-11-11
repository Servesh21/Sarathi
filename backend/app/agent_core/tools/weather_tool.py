"""
Weather Tool for Sarathi Agent
Provides weather information and forecasts for driver planning.
"""
import requests
from typing import Dict, Any
from datetime import datetime
from app.core.config import settings


class WeatherTool:
    """Tool for fetching weather information"""
    
    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    async def get_current_weather(self, location: str) -> Dict[str, Any]:
        """
        Get current weather for a location.
        
        Args:
            location: City name or coordinates
        
        Returns:
            Current weather information
        """
        endpoint = f"{self.base_url}/weather"
        params = {
            "q": location,
            "appid": self.api_key,
            "units": "metric"
        }
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            
            return {
                "success": True,
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"],
                "wind_speed": data["wind"]["speed"],
                "visibility": data.get("visibility", 0) / 1000,  # Convert to km
                "conditions": data["weather"][0]["main"],
                "location": data["name"]
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to fetch weather: {str(e)}"
            }
    
    async def get_weather_forecast(
        self,
        location: str,
        days: int = 3
    ) -> Dict[str, Any]:
        """
        Get weather forecast for upcoming days.
        
        Args:
            location: City name or coordinates
            days: Number of days to forecast (max 5 for free tier)
        
        Returns:
            Weather forecast information
        """
        endpoint = f"{self.base_url}/forecast"
        params = {
            "q": location,
            "appid": self.api_key,
            "units": "metric",
            "cnt": days * 8  # 8 forecasts per day (3-hour intervals)
        }
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            
            forecasts = []
            for item in data["list"]:
                forecasts.append({
                    "datetime": item["dt_txt"],
                    "temperature": item["main"]["temp"],
                    "description": item["weather"][0]["description"],
                    "conditions": item["weather"][0]["main"],
                    "wind_speed": item["wind"]["speed"],
                    "humidity": item["main"]["humidity"]
                })
            
            return {
                "success": True,
                "location": data["city"]["name"],
                "forecasts": forecasts
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to fetch forecast: {str(e)}"
            }
    
    async def check_driving_conditions(self, location: str) -> Dict[str, Any]:
        """
        Analyze weather conditions for driving safety.
        
        Args:
            location: Location to check
        
        Returns:
            Driving condition assessment
        """
        weather = await self.get_current_weather(location)
        
        if not weather["success"]:
            return weather
        
        # Analyze conditions
        conditions = weather["conditions"].lower()
        visibility = weather["visibility"]
        wind_speed = weather["wind_speed"]
        
        # Simple risk assessment
        risk_level = "low"
        warnings = []
        
        if "rain" in conditions or "drizzle" in conditions:
            risk_level = "moderate"
            warnings.append("Wet roads - reduce speed and increase following distance")
        
        if "thunderstorm" in conditions or "snow" in conditions:
            risk_level = "high"
            warnings.append("Severe weather - consider delaying trip if possible")
        
        if visibility < 5:
            risk_level = "moderate" if risk_level == "low" else "high"
            warnings.append("Reduced visibility - use headlights and drive carefully")
        
        if wind_speed > 15:
            warnings.append("Strong winds - be cautious of crosswinds")
        
        return {
            "success": True,
            "risk_level": risk_level,
            "current_conditions": weather["description"],
            "temperature": weather["temperature"],
            "visibility_km": visibility,
            "warnings": warnings,
            "recommendation": "Safe to drive" if risk_level == "low" else "Drive with caution" if risk_level == "moderate" else "Consider delaying trip"
        }


# Tool instance
weather_tool = WeatherTool()
