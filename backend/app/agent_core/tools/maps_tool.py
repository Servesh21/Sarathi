"""
Maps Tool for Sarathi Agent
Provides location-based services including routing, distance calculation, and traffic information.
"""
import requests
from typing import Dict, Any, Optional
from app.core.config import settings


class MapsTool:
    """Tool for interacting with mapping services (Google Maps API)"""
    
    def __init__(self):
        self.api_key = settings.GOOGLE_MAPS_API_KEY
        self.base_url = "https://maps.googleapis.com/maps/api"
    
    async def get_route(
        self,
        origin: str,
        destination: str,
        mode: str = "driving"
    ) -> Dict[str, Any]:
        """
        Get route information between two locations.
        
        Args:
            origin: Starting location (address or coordinates)
            destination: Ending location (address or coordinates)
            mode: Travel mode (driving, walking, bicycling, transit)
        
        Returns:
            Route information including distance, duration, and polyline
        """
        endpoint = f"{self.base_url}/directions/json"
        params = {
            "origin": origin,
            "destination": destination,
            "mode": mode,
            "key": self.api_key
        }
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data["status"] == "OK":
                route = data["routes"][0]
                leg = route["legs"][0]
                
                return {
                    "success": True,
                    "distance": leg["distance"]["text"],
                    "distance_meters": leg["distance"]["value"],
                    "duration": leg["duration"]["text"],
                    "duration_seconds": leg["duration"]["value"],
                    "start_address": leg["start_address"],
                    "end_address": leg["end_address"],
                    "steps": len(leg["steps"])
                }
            else:
                return {
                    "success": False,
                    "error": f"Maps API error: {data['status']}"
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get route: {str(e)}"
            }
    
    async def get_traffic_info(
        self,
        origin: str,
        destination: str
    ) -> Dict[str, Any]:
        """
        Get real-time traffic information for a route.
        
        Args:
            origin: Starting location
            destination: Ending location
        
        Returns:
            Traffic information including duration in traffic
        """
        endpoint = f"{self.base_url}/directions/json"
        params = {
            "origin": origin,
            "destination": destination,
            "departure_time": "now",
            "key": self.api_key
        }
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data["status"] == "OK":
                leg = data["routes"][0]["legs"][0]
                
                return {
                    "success": True,
                    "duration_in_traffic": leg.get("duration_in_traffic", {}).get("text", "N/A"),
                    "duration_in_traffic_seconds": leg.get("duration_in_traffic", {}).get("value", 0),
                    "normal_duration": leg["duration"]["text"],
                    "traffic_delay": leg.get("duration_in_traffic", {}).get("value", 0) - leg["duration"]["value"]
                }
            else:
                return {
                    "success": False,
                    "error": f"Traffic API error: {data['status']}"
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get traffic info: {str(e)}"
            }
    
    async def find_nearby_places(
        self,
        location: str,
        place_type: str = "gas_station",
        radius: int = 5000
    ) -> Dict[str, Any]:
        """
        Find nearby places of a specific type.
        
        Args:
            location: Center location for search
            place_type: Type of place to search for
            radius: Search radius in meters
        
        Returns:
            List of nearby places
        """
        # TODO: Implement nearby places search using Google Places API
        return {
            "success": True,
            "message": "Nearby places search to be implemented",
            "places": []
        }


# Tool instance
maps_tool = MapsTool()
